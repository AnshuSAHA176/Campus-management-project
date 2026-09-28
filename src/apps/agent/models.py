from django.db import models
from pgvector.django import VectorField


class DocumentChunk(models.Model):
    document = models.CharField(max_length=255)

    chunk = models.TextField()

    embedding = VectorField(
        dimensions=1024,
    )

    chunk_index = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["document"]),
        ]

