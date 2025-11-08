from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlalchemy.orm import Session

# Импортируем Pydantic-схему (из app.schemas.category) и зависимость БД
from app.schemas.category import Category 
from app.dependencies import get_db

# Импортируем нашу ORM-модель (из app.models.category)
from app.models.category import Category as CategoryModel 

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)

@router.get("/", response_model=List[Category])
async def read_categories(db: Session = Depends(get_db)):
    """
    Возвращает список только родительских категорий из БД.
    Использует рекурсивную связь для загрузки подкатегорий.
    """
    
    # Запрос к БД: выбираем только те категории, у которых parent_id = NULL
    categories_from_db = db.query(CategoryModel).filter(
        CategoryModel.parent_id.is_(None)
    ).all()

    if not categories_from_db:
        # FastAPI теперь вернет 404, а бот увидит "нет доступных категорий"
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="В базе данных нет доступных категорий."
        )

    return categories_from_db

@router.get("/{category_id}", response_model=Category)
async def read_category(category_id: int, db: Session = Depends(get_db)):
    """Возвращает категорию по ее ID из БД."""
    
    category = db.query(CategoryModel).filter(
        CategoryModel.id == category_id
    ).first()
    
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
        
    return category
