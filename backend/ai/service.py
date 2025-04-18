from backend.config import get_env_settings
from backend.data.service import SalesRepService
from fastapi import Depends
from backend.data.service import get_sales_rep_service
from .utils import SalesRepDocumentProcessor, SalesAnalyticsTools, SalesAnalyticsRetriever

from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.agents import create_structured_chat_agent, AgentExecutor
import os


class RAGChatBotService:
    def __init__(self, sales_rep_service: SalesRepService, llm=None):
        self.sales_data = sales_rep_service.get_all_sales_reps()

        self.llm = llm or ChatGoogleGenerativeAI(model="gemini-2.0-flash-001", temperature=0.2, api_key=get_env_settings().GEMINI_API_KEY)

        # Process documents
        self.documents = SalesRepDocumentProcessor.create_documents_from_sales_data(self.sales_data)

        # Create embeddings model
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        # Create vector store
        self.vectore_store = Chroma.from_documents(documents=self.documents, embedding=self.embeddings)

        # Create custom retriever
        self.retriever = SalesAnalyticsRetriever(sales_data=self.sales_data, vector_store=self.vectore_store)

        # Create analytics tools
        self.analytics_tools = SalesAnalyticsTools(self.sales_data)

        # setup RAG chain
        self._setup_rag_chain()

        # setup agent
        self._setup_agent()

    def _setup_rag_chain(self):
        prompt_template = """
        You are a sales analytics assistant with access to sales representatives data.
        Answer the question based on the following sales representative(s) information:
        
        {context}
        
        Question: {input}
        
        Please answer the question accurately based on the retrieved data. 
        If calculating totals, percentages, or other metrics, show your reasoning step-by-step.
        """

        prompt = PromptTemplate.from_template(prompt_template)
        document_chain = create_stuff_documents_chain(self.llm, prompt)
        self.rag_chain = create_retrieval_chain(self.retriever, document_chain)

    def _setup_agent(self):
        tools = self.analytics_tools.get_tools()
        system_template = """
You are a sales analytics assistant that helps analyze sales rep performance data.
You have access to the following tools:

{tools}

Use these tools to provide accurate information about sales reps, their deals, and clients.
Always use the appropriate tool from: {tool_names}

For comparison questions, make sure to use the comparison tool rather than making separate queries.
When providing financial data, format values with dollar signs and commas.
If calculating or comparing metrics, show your reasoning clearly."""

        agent_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_template),
            HumanMessagePromptTemplate.from_template("{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        agent = create_structured_chat_agent(self.llm, tools, prompt=agent_prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    async def query(self, question: str) -> dict:
        # Analyze the query to determine if it needs specific tools
        query = question.lower()

        # if "compare" in query and any(rep.name.lower() in query for rep in self.sales_data.salesReps):
        #     print("Using comparison tool")
        #     return self.agent_executor.invoke({"input": question})

        # Default to RAG for general queries
        result = self.rag_chain.invoke({"input": question})
        return result


async def get_rag_chatbot_service(sales_rep_sevice=Depends(get_sales_rep_service)):
    """
    Dependency to get the RAGChatBotService instance.
    """
    return RAGChatBotService(sales_rep_service=sales_rep_sevice)
