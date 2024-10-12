from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class ArticleBase(BaseModel):
    title: str
    description: str
    price: float = Field(..., ge=0)  # Cambiado de Decimal a float
    category: str
    condition: str  # Por ejemplo: "nuevo", "usado", "reacondicionado"
    quantity: int = Field(..., ge=0)
    marketplace_id: int  # Añadimos esto para vincular el artículo a un marketplace
    
class ArticleCreate(ArticleBase):
    pass

class ArticleGet(ArticleBase):
    id: int
    created_at: datetime
    seller_uuid: UUID
    status: str  # Por ejemplo: "activo", "vendido", "pausado"
    views: int = 0
    likes: int = 0

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)  # Cambiado de Decimal a float
    category: Optional[str] = None
    condition: Optional[str] = None
    quantity: Optional[int] = Field(None, ge=0)
    status: Optional[str] = None
