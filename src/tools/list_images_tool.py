from langchain.tools import tool
from storage.database.db import get_session
from storage.database.image_manager import ImageManager


@tool
def list_all_images() -> str:
    """查询数据库中保存的所有图片。

    Returns:
        返回所有图片的列表信息
    """
    db = get_session()
    try:
        image_mgr = ImageManager()
        images = image_mgr.get_images(db)

        if not images:
            return "📭 数据库中暂无保存的图片。您可以通过生成图片来创建第一张图片。"

        result = f"📊 数据库中共有 {len(images)} 张图片：\n\n"
        for idx, img in enumerate(images, 1):
            result += f"{idx}. 📌 标题: {img.title}\n"
            result += f"   📝 提示词: {img.prompt}\n"
            result += f"   🔗 图片URL: {img.image_url}\n"
            result += f"   📅 创建时间: {img.created_at}\n\n"

        return result.strip()
    finally:
        db.close()
