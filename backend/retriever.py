import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

DB_DIR = "c:/Users/adars/OneDrive/Desktop/AI-Crisis-War-Room/backend/app/data/chroma_db"

# Initialize embeddings and database connection once (singleton pattern)
print("Loading HuggingFace embeddings for retriever...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

if os.path.exists(DB_DIR):
    print(f"Loading ChromaDB vector store from {DB_DIR}...")
    vector_store = Chroma(
        persist_directory=DB_DIR,
        embedding_function=embeddings
    )
else:
    print(f"WARNING: ChromaDB directory not found at {DB_DIR}. Running with empty database.")
    vector_store = None

def retrieve_context(query: str, top_k: int = 3) -> str:
    """
    Search the ChromaDB vector database for similar chunks and join them.
    """
    if not vector_store:
        return "No crisis management database loaded."
        
    try:
        # Perform similarity search
        results = vector_store.similarity_search(query, k=top_k)
        
        # Merge contents
        context_parts = []
        for i, doc in enumerate(results):
            meta = doc.metadata
            context_parts.append(
                f"[Source: {meta.get('title', 'Unknown')} - Category: {meta.get('category', 'General')}]\n"
                f"{doc.page_content}"
            )
            
        merged_context = "\n\n".join(context_parts)
        return merged_context
    except Exception as e:
        print(f"Error during RAG retrieval search: {e}")
        return f"Error retrieving crisis management context: {str(e)}"

# Standalone execution for testing
if __name__ == "__main__":
    test_query = "ransomware server encryption"
    print(f"\nTesting Retrieval with query: '{test_query}'")
    context = retrieve_context(test_query, top_k=2)
    print("\n--- Retrieved Context ---")
    print(context)
    print("-------------------------")
