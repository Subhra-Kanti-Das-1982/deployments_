from pathlib import Path

import chromadb

from pypdf import PdfReader

from sentence_transformers import (
    SentenceTransformer
)

from config import (
    PDF_DIR,
    VECTOR_DB_DIR,
    EMBEDDING_MODEL
)


def read_pdf(path):

    reader = PdfReader(path)

    pages = []

    for page in reader.pages:

        try:

            text = page.extract_text()

            if text:
                pages.append(text)

        except Exception:
            pass

    return "\n".join(pages)


def chunk_text(
    text,
    chunk_size=1000
):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(
            text[start:end]
        )

        start += chunk_size

    return chunks


def ingest():

    client = chromadb.PersistentClient(
        path=VECTOR_DB_DIR
    )

    collection = (
        client.get_or_create_collection(
            name="mythology"
        )
    )

    if collection.count() > 0:
        return

    model = SentenceTransformer(
        EMBEDDING_MODEL
    )

    idx = 0

    pdfs = list(
        Path(PDF_DIR).glob("*.pdf")
    )

    for pdf in pdfs:

        text = read_pdf(
            str(pdf)
        )

        chunks = chunk_text(text)

        for chunk in chunks:

            embedding = (
                model.encode(chunk)
                .tolist()
            )

            collection.add(
                ids=[str(idx)],
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[
                    {
                        "source":
                        pdf.name
                    }
                ]
            )

            idx += 1

    print(
        f"Indexed {idx} chunks"
    )