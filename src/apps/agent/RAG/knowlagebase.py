from pgvector.django import CosineDistance

from ..models import DocumentChunk
from .embedding import generate_embedding


def knowledge_base(user_query: str) -> list:

    embedding = generate_embedding(user_query)

    knowledge = (
        DocumentChunk.objects
        .annotate(
            distance=CosineDistance("embedding", embedding)
        )
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

    return list(knowledge)