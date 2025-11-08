from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base # Импортируем базовый класс

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True, index=True)

    # Рекурсивная связь для подкатегорий
    subcategories = relationship(
        "Category",
        backref="parent",
        remote_side=[id],
        lazy="selectin"
    )

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"