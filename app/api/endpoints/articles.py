from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID

from app.schemas.article import ArticleCreate, ArticleUpdate, ArticleGet
from app.repository.article_repository import ArticleRepository
from app.utils.utils import get_user

router = APIRouter()

def get_article_repository():
    return ArticleRepository()

@router.post("/", response_model=ArticleGet, status_code=status.HTTP_201_CREATED)
async def create_article(
    article: ArticleCreate,
    repo: ArticleRepository = Depends(get_article_repository),
    user: str = Depends(get_user)
):
    return await repo.create_article(user, article)

@router.get("/{article_id}", response_model=ArticleGet, status_code=status.HTTP_200_OK)
async def get_article(
    article_id: int,
    repo: ArticleRepository = Depends(get_article_repository),
    user: str = Depends(get_user)
):
    article = await repo.get_article(article_id)
    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artículo no encontrado")
    return article

@router.get("/", response_model=List[ArticleGet], status_code=status.HTTP_200_OK)
async def get_all_articles(
    skip: int = 0,
    limit: int = 100,
    repo: ArticleRepository = Depends(get_article_repository),
    user: str = Depends(get_user)
):
    return await repo.get_all_articles(skip=skip, limit=limit)

@router.put("/{article_id}", response_model=ArticleGet, status_code=status.HTTP_200_OK)
async def update_article(
    article_id: int,
    article_update: ArticleUpdate,
    repo: ArticleRepository = Depends(get_article_repository),
    user: str = Depends(get_user)
):
    existing_article = await repo.get_article(article_id)
    if existing_article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artículo no encontrado")
    if str(existing_article.seller_uuid) != user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para actualizar este artículo")
    
    updated_article = await repo.update_article(article_id, article_update)
    return updated_article

@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    article_id: int,
    repo: ArticleRepository = Depends(get_article_repository),
    user: str = Depends(get_user)
):
    existing_article = await repo.get_article(article_id)
    if existing_article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artículo no encontrado")
    if str(existing_article.seller_uuid) != user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para eliminar este artículo")
    
    success = await repo.delete_article(article_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No se pudo eliminar el artículo")
    return None

@router.get("/seller/{seller_uuid}", response_model=List[ArticleGet], status_code=status.HTTP_200_OK)
async def get_seller_articles(
    seller_uuid: UUID,
    repo: ArticleRepository = Depends(get_article_repository),
    user: str = Depends(get_user)
):
    if str(seller_uuid) != user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para ver los artículos de otros vendedores")
    return await repo.get_seller_articles(seller_uuid)
