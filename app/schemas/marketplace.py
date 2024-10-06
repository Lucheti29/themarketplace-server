from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class MarketplaceBase(BaseModel):
    title: str
    description: Optional[str] = None


class MarketplaceGet(MarketplaceBase):
    id: int
    created_at: datetime
    title: str
    description: Optional[str] = None
    owner_uuid: UUID


class MarketplaceCreate(MarketplaceBase):
    pass


class MarketplaceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None