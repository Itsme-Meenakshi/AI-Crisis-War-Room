from sentence_transformers import SentenceTransformer

# =====================================================
# Embedding Model
# =====================================================

# Lightweight sentence embedding model used for
# semantic similarity and retrieval.

model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text: str):
    """
    Generate an embedding vector for a given text.

    Args:
        text (str): Input text.

    Returns:
        list: Embedding vector.
    """
    return model.encode(text).tolist()