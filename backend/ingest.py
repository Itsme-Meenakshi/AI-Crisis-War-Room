import os
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

DOCS_DIR = "c:/Users/adars/OneDrive/Desktop/AI-Crisis-War-Room/backend/app/data/documents"
DB_DIR = "c:/Users/adars/OneDrive/Desktop/AI-Crisis-War-Room/backend/app/data/chroma_db"
CHUNKS_JSON_PATH = "c:/Users/adars/OneDrive/Desktop/AI-Crisis-War-Room/backend/chunks.json"

def run_ingestion():
    print("Initializing RAG Ingestion Pipeline...")
    
    # 1. Load files
    documents = []
    if not os.path.exists(DOCS_DIR):
        raise FileNotFoundError(f"Documents directory not found at {DOCS_DIR}")
        
    for filename in os.listdir(DOCS_DIR):
        if filename.endswith(".txt"):
            file_path = os.path.join(DOCS_DIR, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                # Parse metadata from file lines
                title = lines[0].replace("Title: ", "").strip()
                category = lines[1].replace("Category: ", "").strip()
                doc_id = lines[2].replace("Document ID: ", "").strip()
                content = "".join(lines[3:]).replace("Content: ", "").strip()
                
                documents.append({
                    "text": content,
                    "metadata": {
                        "source": filename,
                        "title": title,
                        "category": category,
                        "doc_id": doc_id
                    }
                })
                
    print(f"Loaded {len(documents)} documents.")
    
    # 2. Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len
    )
    
    chunks_to_embed = []
    chunks_records = []
    chunk_idx = 1
    
    for doc in documents:
        splits = text_splitter.split_text(doc["text"])
        for split in splits:
            chunk_id = f"chunk_{chunk_idx:04d}"
            # Format for database injection
            chunks_to_embed.append({
                "page_content": split,
                "metadata": doc["metadata"]
            })
            # Format for chunks.json log
            chunks_records.append({
                "chunk_id": chunk_id,
                "text": split,
                "metadata": doc["metadata"]
            })
            chunk_idx += 1
            
    print(f"Split documents into {len(chunks_to_embed)} chunks.")
    
    # 3. Initialize Embedding Model
    # all-MiniLM-L6-v2 is a fast and lightweight sentence transformer
    print("Loading HuggingFace sentence-transformers embedding model...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # 4. Initialize and Populate Chroma DB
    print(f"Connecting to ChromaDB and storing embeddings in {DB_DIR}...")
    
    # Extract page contents and metadata lists
    texts = [c["page_content"] for c in chunks_to_embed]
    metadatas = [c["metadata"] for c in chunks_to_embed]
    
    # Create the vector database
    db = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory=DB_DIR
    )
    
    print("ChromaDB vector store successfully created.")
    
    # 5. Serialize chunks to chunks.json
    print(f"Writing chunks serialization file to {CHUNKS_JSON_PATH}...")
    with open(CHUNKS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks_records, f, indent=2)
        
    print("RAG Ingestion Pipeline completed successfully!")

if __name__ == "__main__":
    run_ingestion()
