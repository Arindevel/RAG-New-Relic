from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

# -----------------------------
# 1. Load embeddings
# -----------------------------

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)

# -----------------------------
# 2. Load ChromaDB
# -----------------------------

vector_store = Chroma(
    collection_name="new_relic_knowledge",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

# -----------------------------
# 3. Create retriever
# -----------------------------

retriever = vector_store.as_retriever(
    search_kwargs={"k": 2}
)

# -----------------------------
# 4. Load Gemini
# -----------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash"
)

# -----------------------------
# 5. Ask question
# -----------------------------

question = input("\nAsk your New Relic question: ")

# Retrieve relevant documents
docs = retriever.invoke(question)

print("\n--- Retrieved Documents ---")

for i, doc in enumerate(docs, 1):
    print(f"\nDocument {i}")
    print("Source:", doc.metadata.get("source"))
    print(doc.page_content)

# -----------------------------
# 6. Build context
# -----------------------------

context = "\n\n".join(
    doc.page_content for doc in docs
)

prompt = f"""
You are a New Relic troubleshooting assistant.

Answer the user's question using ONLY the information
provided in the context below.

If the answer cannot be found in the context,
say: "I don't have enough information in the knowledge base."

Context:
{context}

User question:
{question}

Provide a clear and concise answer.
"""

# -----------------------------
# 7. Generate answer
# -----------------------------

response = llm.invoke(prompt)

print("\n--- AI Answer ---")

if isinstance(response.content, list):
    for item in response.content:
        if isinstance(item, dict) and item.get("type") == "text":
            print(item.get("text", ""))
else:
    print(response.content)
