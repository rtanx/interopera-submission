from backend.config import get_env_settings
from backend.data.service import SalesRepService
from fastapi import Depends
from backend.data.service import get_sales_rep_service

from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter
import os


class RAGChatBotService:
    def __init__(self, sales_rep_service: SalesRepService):
        sales_reps = sales_rep_service.get_all_sales_reps()

        # convert each SalesRep into a langchain document
        docs = []
        for rep in sales_reps:
            rep_info = (
                f"Name: {rep.name}\n"
                f"Role: {rep.role}\n"
                f"Region: {rep.region}\n"
                f"Skills: {', '.join(rep.skills)}\n"
            )

            deals_info = "Deals:\n" + "\n".join(
                [f"Client: {deal.client}, Value: {deal.value}, Status: {deal.status}" for deal in rep.deals]
            )

            clients_info = "Clients:\n" + "\n".join(
                [f"Name: {client.name}, Industry: {client.industry}, Contact: {client.contact}" for client in rep.clients]
            )

            combined_text = f"{rep_info}\n{deals_info}\n\n{clients_info}"

            docs.append(Document(page_content=combined_text, metadata={"name": rep.name, "id": rep.id}))

        # split document into smaller chunks
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        split_docs = text_splitter.split_documents(docs)

        # create vector store using embeddings
        embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = FAISS.from_documents(split_docs, embeddings_model)
        retriever = vectorstore.as_retriever()

        # setup Gemini LLM and RetrivalQA chain
        gemini_api_key = get_env_settings().GEMINI_API_KEY
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001", temperature=0.2, api_key=gemini_api_key)
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
        )

    async def query(self, question: str) -> dict:
        result = self.qa_chain({"query": question})
        return {
            "answer": result["result"],
            "source": [doc.metadata.get("name", "unknown") for doc in result["source_documents"]]
        }


async def get_rag_chatbot_service(sales_rep_sevice=Depends(get_sales_rep_service)):
    """
    Dependency to get the RAGChatBotService instance.
    """
    return RAGChatBotService(sales_rep_service=sales_rep_sevice)
