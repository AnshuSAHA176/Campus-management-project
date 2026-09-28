import pymupdf

import nltk
from nltk.tokenize import sent_tokenize

nltk.download("punkt")


def chunking(document_name):
    doc = pymupdf.open("a.pdf")
    # sentecne
    sentences = []
    for page_number, page in enumerate(doc, start=1):
        text = page.get_text().encode("utf8")
        if not text.strip():
            continue
        page_sentence = sent_tokenize(text)
        for sentence in page_sentence:
            if not sentence.strip():
                continue
            sentences.append(
                {
                    "page": page_number,
                    "text": sentence
                }
            )

    doc.close()


