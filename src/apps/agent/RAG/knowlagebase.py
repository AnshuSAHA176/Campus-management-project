from pgvector.django import CosineDistance

from ..models import DocumentChunk
from .embedding import generate_embedding


import asyncio
from asgiref.sync import sync_to_async

def _search_chunks(embedding):
    return list(
        DocumentChunk.objects
        .annotate(distance=CosineDistance("embedding", embedding))
        .filter(document__status="DONE")
        .order_by("distance")
        .values(
            "document_id",
            "document__title",
            "chunk",
            "page_start",
            "page_end",
        )[:2]
    )

async def knowledge_base(user_query: str) -> list:
    embedding = await asyncio.to_thread(generate_embedding, user_query)
    return await sync_to_async(_search_chunks)(embedding)