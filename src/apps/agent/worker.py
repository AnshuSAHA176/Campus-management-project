from celery import shared_task

from .models import Document, DocumentChunk

import requests
import tempfile

from .RAG.chunking import chunking
from .RAG.embedding import generate_embedding


@shared_task(bind=True, ignore_result=True)
def document_upload_to_vector(self, doc_id):

    doc = Document.objects.get(id=doc_id)

    doc.status = "PROCESSING"
    doc.save(update_fields=["status"])

    try:
        pdf_url = doc.file.url.replace("http://", "https://")

        response = requests.get(
            pdf_url,
            timeout=60,
        )

        response.raise_for_status()

        with tempfile.NamedTemporaryFile(
            suffix=".pdf"
        ) as temp_file:

            temp_file.write(response.content)
            temp_file.flush()

            chunks = chunking(temp_file.name)

            for i, chunk in enumerate(chunks):

                embedding = generate_embedding(
                    chunk["text"]
                )

                DocumentChunk.objects.create(
                    document=doc,
                    chunk=chunk["text"],
                    embedding=embedding,
                    chunk_index=i,
                    page_start=chunk["page_start"],
                    page_end=chunk["page_end"],
                )

        doc.status = "DONE"
        doc.save(update_fields=["status"])

    except Exception:
        doc.status = "FAILED"
        doc.save(update_fields=["status"])
        raise