import os
import chromadb

# =====================================================
# Paths
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

CHROMA_PATH = os.path.join(
    BASE_DIR,
    "knowledge_base",
    "chroma_db"
)

# =====================================================
# ChromaDB
# =====================================================

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_collection(
    "crisis_knowledge"
)

# =====================================================
# Retrieve Documents
# =====================================================

def retrieve(query: str, top_k: int = 3, category: str = None):
    """
    Retrieve the most relevant documents from ChromaDB.

    Args:
        query (str): User query.
        top_k (int): Number of documents to retrieve.
        category (str, optional): Restrict search to a specific category.

    Returns:
        list: List of retrieved documents with metadata.
    """

    if category:
        results = collection.query(
            query_texts=[query],
            n_results=top_k,
            where={"category": category}
        )
    else:
        results = collection.query(
            query_texts=[query],
            n_results=top_k
        )

    if not results["documents"] or not results["documents"][0]:
        return []

    retrieved = []

    for doc, metadata in zip(
        results["documents"][0],
        results["metadatas"][0]
    ):
        retrieved.append({
            "text": doc,
            "source": metadata.get("source"),
            "category": metadata.get("category"),
            "file_type": metadata.get("file_type")
        })

    return retrieved