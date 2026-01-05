from langchain.tools import tool
from storage.database.db import get_session
from storage.database.image_manager import ImageManager, ImageCreate


@tool
def generate_and_save_image(title: str, prompt: str) -> str:
    """根据标题和提示词生成图片，并保存到数据库中。

    Args:
        title: 图片标题，用于后续查询
        prompt: 图片生成提示词，描述想要生成的图片内容

    Returns:
        返回生成的图片信息和保存结果
    """
    ctx = None  # 上下文对象

    try:
        from cozeloop.decorator import observe
        from coze_coding_utils.runtime_ctx.context import Context

        # 定义带装饰器的生成函数
        @observe
        def image_generation_wrapper(ctx: Context, prompt: str, size: str = "2K") -> tuple:
            from coze_coding_utils.runtime_ctx.context import default_headers
            import requests
            import os

            api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
            base_url = os.getenv("COZE_INTEGRATION_BASE_URL")
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            }
            headers.update(default_headers(ctx))

            request = {
                "model": "doubao-seedream-4-5-251128",
                "prompt": prompt,
                "size": size,
                "watermark": True,
                "response_format": "url",
                "optimize_prompt_options": {
                    "mode": "standard",
                },
                "sequential_image_generation": "disabled",
            }

            response = requests.post(
                f'{base_url}/api/v3/images/generations',
                json=request,
                headers=headers
            )

            response.raise_for_status()
            data = response.json()

            if "error" in data:
                raise Exception(
                    f"图片生成失败: code={data.get('error', {}).get('code')}, message={data.get('error', {}).get('message')}")

            # 提取图片 URL
            if not data.get("data") or len(data["data"]) == 0:
                raise Exception("生成的图片数据为空")

            image_url = data["data"][0].get("url")
            if not image_url:
                raise Exception("未能获取到图片URL")

            return image_url, data

        # 存储生成的图片信息
        saved_images = []
        db = get_session()
        
        try:
            image_mgr = ImageManager()
            # 循环两次，生成并存储两张图片
            for i in range(2):
                # 调用图片生成
                image_url, _ = image_generation_wrapper(ctx, prompt)
                
                # 保存到数据库
                image_mgr.create_image(
                    db,
                    ImageCreate(
                        title=title,
                        prompt=prompt,
                        image_url=image_url
                    )
                )
                saved_images.append(image_url)
                
            image_list_str = "\n".join([f"🖼️ 图片{i+1} URL: {url}" for i, url in enumerate(saved_images)])
            return f"✅ 两张图片生成成功！\n\n📌 基础标题: {title}\n📝 提示词: {prompt}\n{image_list_str}\n\n图片已保存到数据库，您可以通过标题查询这些图片。"
            
        finally:
            db.close()

    except Exception as e:
        return f"❌ 生成图片失败: {str(e)}"
