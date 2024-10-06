from app.schemas.marketplace import MarketplaceCreate, MarketplaceGet, MarketplaceUpdate

from supabase import create_client, Client

import os
from supabase import create_client, Client
from dotenv import load_dotenv
from typing import List

class MarketplaceRepository:
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.client: Client = create_client(self.supabase_url, self.supabase_key)


    def get_marketplaces(self) -> List[MarketplaceGet]:
        response = self.client.table('marketplaces').select('*').execute()
        marketplaces = [MarketplaceGet(**marketplace) for marketplace in response.data]
        return marketplaces


    def get_marketplace_by_id(self, marketplace_id: int) -> MarketplaceGet:
        response = self.client.table('marketplaces').select('*').eq('id', marketplace_id).execute()
        return MarketplaceGet(**response.data[0])


    def create_marketplace(self, user_id: str, marketplace_data: MarketplaceCreate) -> MarketplaceGet:
        data = {
            'title': marketplace_data.title,
            'description': marketplace_data.description,
            'owner_uuid': user_id
        }

        response = self.client.table('marketplaces').insert(data).execute()
        return MarketplaceGet(**response.data[0])


    def update_marketplace(self, marketplace_id: int, marketplace_data: MarketplaceUpdate) -> MarketplaceGet:
        response = self.client.table('marketplaces').update(marketplace_data.dict(exclude_unset=True)).eq('id', marketplace_id).execute()
        return MarketplaceGet(**response.data[0])


    def delete_marketplace(self, marketplace_id: int):
        response = self.client.table('marketplaces').delete().eq('id', marketplace_id).execute()
        return MarketplaceGet(**response.data[0])