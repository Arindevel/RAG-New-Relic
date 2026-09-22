from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)

result = embeddings.embed_query("New Relic APM troubleshooting")

print("Embedding type:", type(result))
print("Embedding length:", len(result))
print("First 5 values:", result[:5])
