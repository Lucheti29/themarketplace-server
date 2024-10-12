from app.schemas.article import ArticleCreate, ArticleGet, ArticleUpdate
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from typing import List, Optional
from uuid import UUID

class ArticleRepository:
    def __init__(self):
        load_dotenv()
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.client: Client = create_client(self.supabase_url, self.supabase_key)

    async def create_article(self, user: str, article: ArticleCreate) -> ArticleGet:
        data = article.dict()
        data['seller_uuid'] = user
        response = self.client.table('articles').insert(data).execute()
        return ArticleGet(**response.data[0])

    async def get_article(self, article_id: int) -> Optional[ArticleGet]:
        response = self.client.table('articles').select('*').eq('id', article_id).execute()
        if response.data:
            return ArticleGet(**response.data[0])
        return None

    async def get_all_articles(self, skip: int = 0, limit: int = 100) -> List[ArticleGet]:
        response = self.client.table('articles').select('*').range(skip, skip + limit - 1).execute()
        return [ArticleGet(**article) for article in response.data]

    async def update_article(self, article_id: int, article_update: ArticleUpdate) -> Optional[ArticleGet]:
        update_data = article_update.dict(exclude_unset=True)
        response = self.client.table('articles').update(update_data).eq('id', article_id).execute()
        if response.data:
            return ArticleGet(**response.data[0])
        return None

    async def delete_article(self, article_id: int) -> bool:
        response = self.client.table('articles').delete().eq('id', article_id).execute()
        return len(response.data) > 0

    async def get_seller_articles(self, seller_uuid: UUID) -> List[ArticleGet]:
        response = self.client.table('articles').select('*').eq('seller_uuid', str(seller_uuid)).execute()
        return [ArticleGet(**article) for article in response.data]

    async def get_marketplace_articles(self, marketplace_id: int, skip: int = 0, limit: int = 100) -> List[ArticleGet]:
        response = self.client.table('articles').select('*').eq('marketplace_id', marketplace_id).range(skip, skip + limit - 1).execute()
        return [ArticleGet(**article) for article in response.data]
