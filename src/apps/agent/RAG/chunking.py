import pymupdf
import numpy as np
import nltk

from nltk.tokenize import sent_tokenize

from .embedding import generate_embedding


def chunking(document_name):

    doc = pymupdf.open(document_name)

    sentences = []

    for page_number, page in enumerate(doc, start=1):

        text = page.get_text()

        if not text.strip():
            continue

        page_sentences = sent_tokenize(text)

        for sentence in page_sentences:

            sentence = sentence.strip()

            if not sentence:
                continue

            sentences.append({
                "page": page_number,
                "text": sentence,
            })

    doc.close()

    if len(sentences) < 2:
        return sentences

    # Generate embeddings
    sentence_embeddings = [
        generate_embedding(sentence["text"])
        for sentence in sentences
    ]

    # Convert to numpy array
    sentence_embeddings = np.array(
        sentence_embeddings,
        dtype=np.float32,
    )

    # Normalize embeddings
    norms = np.linalg.norm(
        sentence_embeddings,
        axis=1,
        keepdims=True,
    )

    sentence_embeddings = (
        sentence_embeddings / np.maximum(norms, 1e-12)
    )

    # Adjacent sentence similarity
    similarities = []

    for i in range(len(sentence_embeddings) - 1):

        similarity = np.dot(
            sentence_embeddings[i],
            sentence_embeddings[i + 1],
        )

        similarities.append(float(similarity))

    similarities = np.array(similarities)

    # Low similarity = possible topic boundary
    threshold = np.percentile(
        similarities,
        20,
    )

    boundaries = []

    for i, similarity in enumerate(similarities):

        if similarity <= threshold:
            boundaries.append(i + 1)

    # Create chunks
    chunks = []

    start = 0

    for boundary in boundaries:

        chunk_sentences = sentences[start:boundary]

        chunk_text = " ".join(
            sentence["text"]
            for sentence in chunk_sentences
        )

        chunks.append({
            "text": chunk_text,
            "page_start": chunk_sentences[0]["page"],
            "page_end": chunk_sentences[-1]["page"],
        })

        start = boundary

    # Remaining sentences
    if start < len(sentences):

        chunk_sentences = sentences[start:]

        chunk_text = " ".join(
            sentence["text"]
            for sentence in chunk_sentences
        )

        chunks.append({
            "text": chunk_text,
            "page_start": chunk_sentences[0]["page"],
            "page_end": chunk_sentences[-1]["page"],
        })

    return chunks