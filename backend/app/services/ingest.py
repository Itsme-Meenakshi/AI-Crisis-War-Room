import os
import json
import chromadb

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# =====================================================
# Paths
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DOCS_PATH = os.path.join(
    BASE_DIR,
    "knowledge_base",
    "documents"
)

CHROMA_PATH = os.path.join(
    BASE_DIR,
    "knowledge_base",
    "chroma_db"
)

# =====================================================
# ChromaDB
# =====================================================

client = chromadb.PersistentClient(path=CHROMA_PATH)

# Recreate the collection every time to avoid duplicates
try:
    client.delete_collection("crisis_knowledge")
except Exception:
    pass

collection = client.create_collection(
    name="crisis_knowledge"
)

# =====================================================
# Text Splitter
# =====================================================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

all_chunks = []

# =====================================================
# Read Documents
# =====================================================

for root, dirs, files in os.walk(DOCS_PATH):

    for filename in files:

        filepath = os.path.join(root, filename)

        text = ""

        # -----------------------------
        # TXT Files
        # -----------------------------
        if filename.lower().endswith(".txt"):

            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()

        # -----------------------------
        # PDF Files
        # -----------------------------
        elif filename.lower().endswith(".pdf"):

            try:
                reader = PdfReader(filepath)

                for page in reader.pages:

                    extracted = page.extract_text()

                    if extracted:
                        text += extracted + "\n"

            except Exception as e:
                print(f"⚠️ Skipping {filename}: {e}")
                continue

        else:
            continue

        # Skip empty documents
        if not text.strip():
            continue

        # Split into chunks
        chunks = splitter.split_text(text)

        for i, chunk in enumerate(chunks):

            chunk_id = f"{filename}_{i}"

            metadata = {
                "source": filename,
                "category": os.path.basename(root),
                "file_type": os.path.splitext(filename)[1].replace(".", "")
            }

            collection.add(
                ids=[chunk_id],
                documents=[chunk],
                metadatas=[metadata]
            )

            all_chunks.append({
                "id": chunk_id,
                "source": metadata["source"],
                "category": metadata["category"],
                "file_type": metadata["file_type"],
                "text": chunk
            })

# =====================================================
# Save Chunk Information
# =====================================================

chunks_file = os.path.join(
    BASE_DIR,
    "knowledge_base",
    "chunks.json"
)

with open(
    chunks_file,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_chunks,
        f,
        indent=4,
        ensure_ascii=False
    )

# =====================================================
# Success Message
# =====================================================

print("=" * 60)
print("✅ Knowledge Base Created Successfully!")
print(f"📄 Total Chunks Stored : {len(all_chunks)}")
print(f"📂 Database Location   : {CHROMA_PATH}")
print("=" * 60)