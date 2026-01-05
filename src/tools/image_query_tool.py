from langchain.tools import tool
from storage.database.db import get_session
from storage.database.image_manager import ImageManager


@tool
def query_image_by_title(title: str) -> str:
    """根据标题查询数据库中保存的图片。

    Args:
        title: 要查询的图片标题

    Returns:
        返回图片的详细信息，包括标题、提示词和图片URL
    """
    db = get_session()
    try:
        image_mgr = ImageManager()
        images = image_mgr.get_images_by_title(db, title)

        if images:
            result = f"🖼️ 找到 {len(images)} 张匹配的图片！\n\n"
            for idx, image in enumerate(images, 1):
                result += f"【图片 {idx}】\n"
                result += f"📌 标题: {image.title}\n"
                result += f"📝 提示词: {image.prompt}\n"
                result += f"🔗 图片URL: {image.image_url}\n"
                result += f"📅 创建时间: {image.created_at}\n\n"
            return result.strip()
        else:
            return f"❌ 未找到标题为「{title}」的图片。请检查标题是否正确，或者先生成一张新图片。"
    finally:
        db.close()
