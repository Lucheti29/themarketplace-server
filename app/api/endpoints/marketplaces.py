## Create endpoints for creation and get marketplaces

from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.marketplace import MarketplaceCreate, MarketplaceUpdate, MarketplaceGet
from app.repository.marketplace_repository import MarketplaceRepository
from app.utils.utils import get_user

router = APIRouter()

# Check
@router.post("/", response_model=MarketplaceGet, status_code=status.HTTP_201_CREATED)
def create_marketplace(marketplace: MarketplaceCreate, user: str = Depends(get_user)):
    marketplace_repo = MarketplaceRepository()
    return marketplace_repo.create_marketplace(user, marketplace)

# Check
@router.get("/{marketplace_id}", response_model=MarketplaceGet, status_code=status.HTTP_200_OK)
def get_marketplace(marketplace_id: int, user: str = Depends(get_user)):
    marketplace_repo = MarketplaceRepository()
    return marketplace_repo.get_marketplace_by_id(marketplace_id)


@router.get("/", response_model=list[MarketplaceGet], status_code=status.HTTP_200_OK)
def get_all_marketplaces(user: str = Depends(get_user)):
    marketplace_repo = MarketplaceRepository()
    return marketplace_repo.get_marketplaces()


@router.put("/{marketplace_id}", response_model=MarketplaceGet, status_code=status.HTTP_200_OK)
def update_marketplace(marketplace_id: int, marketplace: MarketplaceUpdate, user: str = Depends(get_user)):
    marketplace_repo = MarketplaceRepository()
    return marketplace_repo.update_marketplace(marketplace_id, marketplace)


@router.delete("/{marketplace_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_marketplace(marketplace_id: int, user: str = Depends(get_user)):
    marketplace_repo = MarketplaceRepository()
    marketplace_repo.delete_marketplace(marketplace_id)