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
        image = image_mgr.get_image_by_title(db, title)

        if image:
            return f"🖼️ 找到图片！\n\n📌 标题: {image.title}\n📝 提示词: {image.prompt}\n🔗 图片URL: {image.image_url}\n📅 创建时间: {image.created_at}"
        else:
            return f"❌ 未找到标题为「{title}」的图片。请检查标题是否正确，或者先生成一张新图片。"
    finally:
        db.close()
