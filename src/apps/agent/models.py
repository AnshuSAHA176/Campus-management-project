from django.db import models
from pgvector.django import VectorField
from cloudinary.models import CloudinaryField
import uuid

class Document(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    title = models.CharField(max_length=255)

    file = CloudinaryField(
        "file",
        resource_type="raw",
    )

    document_type = models.CharField(max_length=100)

    year = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        default="pending",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )


class DocumentChunk(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="chunks",
    )

    chunk = models.TextField()

    embedding = VectorField(
        dimensions=1024,
    )

    chunk_index = models.PositiveIntegerField()

    page_start = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    page_end = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
