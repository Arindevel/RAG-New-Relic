import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

st.set_page_config(
    page_title="New Relic RAG Assistant",
    page_icon="🔍"
)

st.title("🔍 New Relic Troubleshooting Assistant")
st.write("Ask questions about New Relic application troubleshooting.")

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)

vector_store = Chroma(
    collection_name="new_relic_knowledge",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 2}
)

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash"
)

question = st.text_input(
    "Ask your New Relic question:"
)

if question:

    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    prompt = f"""
You are a New Relic troubleshooting assistant.

Answer the user's question using ONLY the information
provided in the context below.

If the answer cannot be found in the context,
say:

"I don't have enough information in the knowledge base."

Context:
{context}

User question:
{question}

Provide a clear and concise answer.
"""

    response = llm.invoke(prompt)

    if isinstance(response.content, list):
        answer = ""
        for item in response.content:
            if isinstance(item, dict) and item.get("type") == "text":
                answer += item.get("text", "")
    else:
        answer = response.content

    st.subheader("🤖 AI Answer")
    st.write(answer)

    st.subheader("📚 Sources")

    for doc in docs:
        st.write(
            f"**{doc.metadata.get('source')}**"
        )
