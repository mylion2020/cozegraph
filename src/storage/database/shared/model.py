from sqlalchemy import Column, DateTime, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, comment="图片ID")
    title = Column(String(255), nullable=False, comment="图片标题")
    prompt = Column(Text, nullable=False, comment="生成图片的提示词")
    image_url = Column(String(2048), nullable=False, comment="生成的图片URL")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment="创建时间")

