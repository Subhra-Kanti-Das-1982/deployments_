import chromadb

from sentence_transformers import (
    SentenceTransformer
)

from config import (
    VECTOR_DB_DIR,
    EMBEDDING_MODEL,
    TOP_K
)

client = chromadb.PersistentClient(
    path=VECTOR_DB_DIR
)

collection = (
    client.get_or_create_collection(
        name="mythology"
    )
)

embedder = SentenceTransformer(
    EMBEDDING_MODEL
)


def retrieve(query):

    embedding = (
        embedder.encode(query)
        .tolist()
    )

    result = collection.query(
        query_embeddings=[
            embedding
        ],
        n_results=TOP_K
    )

    docs = result["documents"][0]

    meta = result["metadatas"][0]

    return docs, meta