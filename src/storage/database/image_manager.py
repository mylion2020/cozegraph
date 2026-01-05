from typing import List, Optional
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from storage.database.shared.model import Image

# --- Pydantic Models ---
class ImageCreate(BaseModel):
    title: str = Field(..., description="图片标题")
    prompt: str = Field(..., description="生成图片的提示词")
    image_url: str = Field(..., description="生成的图片URL")


# --- Manager Class ---
class ImageManager:
    """Manager class for Image operations."""

    def create_image(self, db: Session, image_in: ImageCreate) -> Image:
        """创建新的图片记录."""
        image_data = image_in.model_dump()
        db_image = Image(**image_data)
        db.add(db_image)
        try:
            db.commit()
            db.refresh(db_image)
            return db_image
        except Exception:
            db.rollback()
            raise

    def get_images_by_title(self, db: Session, title: str) -> List[Image]:
        """根据标题查询所有匹配的图片."""
        return db.query(Image).filter(Image.title == title).all()

    def get_images(self, db: Session, skip: int = 0, limit: int = 100) -> List[Image]:
        """获取所有图片列表."""
        return db.query(Image).order_by(Image.created_at.desc()).offset(skip).limit(limit).all()

    def delete_images_by_title(self, db: Session, title: str) -> int:
        """根据标题删除图片."""
        deleted_count = db.query(Image).filter(Image.title == title).delete()
        db.commit()
        return deleted_count
