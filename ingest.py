from pathlib import Path

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

# -----------------------------
# 1. Load documents
# -----------------------------

documents = []

for file_path in Path("documents").glob("*.txt"):
    text = file_path.read_text(encoding="utf-8")

    documents.append(
        Document(
            page_content=text,
            metadata={"source": file_path.name}
        )
    )

print(f"Loaded {len(documents)} documents")

# -----------------------------
# 2. Split into chunks
# -----------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks")

# -----------------------------
# 3. Create embeddings
# -----------------------------

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)

# Test embedding before Chroma
test_vector = embeddings.embed_query("New Relic APM")

print(f"Embedding dimension: {len(test_vector)}")

# -----------------------------
# 4. Create ChromaDB
# -----------------------------

vector_store = Chroma(
    collection_name="new_relic_knowledge",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

# -----------------------------
# 5. Add documents
# -----------------------------

vector_store.add_documents(chunks)

print("✅ Documents successfully stored in ChromaDB!")
