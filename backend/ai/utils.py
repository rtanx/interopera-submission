from typing import List, Optional, Any
from pydantic import BaseModel
from backend.data.schemas import SalesRep, Deal, Client, SalesData
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.tools import tool, Tool
from .schemas import ToolSchema_RepName, ToolSchema_CompareReps


class SalesRepDocumentProcessor:
    """Helper class to process sales rep data into LangChain documents."""

    @staticmethod
    def format_deals(deals: List[Deal]) -> str:
        """Format deals into a string representation."""
        if not deals:
            return "No deals available."

        result = ""

        for deal in deals:
            result += f"- Client: {deal.client}, Value: {deal.value}, Status: {deal.status}\n"

        return result

    @staticmethod
    def format_clients(clients: List[Client]) -> str:
        """Format clients into a readable text representation."""
        if not clients:
            return "No clients available."

        result = ""

        for client in clients:
            result += f"- Name: {client.name}, Industry: {client.industry}, Contact: {client.contact}\n"

        return result

    @classmethod
    def create_document_from_rep(cls, rep: SalesRep) -> str:
        """Convert a single rep model to a LangChain document."""
        metadata = {
            "rep_id": rep.id,
            "rep_name": rep.name,
            "rep_role": rep.role,
            "rep_region": rep.region,
            "document_type": "sales_rep",
        }

        content = f"""
        Sales Rep: {rep.name}
        ID: {rep.id}
        Role: {rep.role}
        Region: {rep.region}
        Skills: {', '.join(rep.skills)}
        
        Deals:
        {cls.format_deals(rep.deals)}
        
        Clients:
        {cls.format_clients(rep.clients)}
        """

        return Document(page_content=content, metadata=metadata)

    @classmethod
    def create_documents_from_sales_data(cls, sales_data: SalesData) -> List[Document]:
        """Convert all sales reps in sales data to LangChain documents"""
        return [cls.create_document_from_rep(rep) for rep in sales_data.salesReps]


class SalesAnalyticsRetriever(BaseRetriever, BaseModel):
    """
    Custom retriever to fetch documents based on sales data. 
    Combines vector search with direct Pydantic model access.
    """
    sales_data: SalesData
    vector_store: Chroma

    class Config:
        arbitrary_types_allowed = True

    def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun) -> List[Document]:
        """
        Get relevant documents based on the query using both vector search and model access
        """
        vector_docs = self.vector_store.similarity_search(query, k=5)

        for rep in self.sales_data.salesReps:
            if rep.name.lower() in query.lower():
                rep_doc = SalesRepDocumentProcessor.create_document_from_rep(rep)
                if not any(d.metadata.get("rep_id") == rep.id for d in vector_docs):
                    vector_docs.append(rep_doc)

        return vector_docs


class SalesAnalyticsTools:

    def __init__(self, sales_data: SalesData):
        """Initialize the tools with sales data."""
        self.sales_data = sales_data
        self.sales_reps_by_name = {rep.name.lower(): rep for rep in sales_data.salesReps}

    def _get_rep_by_name(self, rep_name: str) -> str:
        return self.sales_reps_by_name.get(rep_name.lower())

    def get_rep_performance(self, rep_name: str) -> str:
        rep = self._get_rep_by_name(rep_name)
        if not rep:
            return f"Sales representative {rep_name} not found."

        # calculate performance metrics
        statuses_count = rep.deal_count_by_status()
        total_value = sum(deal.value for deal in rep.deals)

        return f"""
        Performance for {rep.name} ({rep.role}, {rep.region}):
        - Region: {rep.region}
        - Total Deals: {len(rep.deals)}
        - Closed Won: {statuses_count.get("Closed Won", 0)}
        - Closed Lost: {statuses_count.get("Closed Lost", 0)}
        - In Progress: {statuses_count.get("In Progress", 0)}
        - Win rate: {rep.win_rate():.1f}%
        - Total pipeline value: {total_value:,.2f}
        """

    def compare_reps(self, rep1_name: str, rep2_name: str) -> str:
        """
        Compare performance of two sales reps.
        """

        rep1 = self._get_rep_by_name(rep1_name)
        rep2 = self._get_rep_by_name(rep2_name)

        if not rep1:
            return f"Sales representative {rep1_name} not found."
        if not rep2:
            return f"Sales representative {rep2_name} not found."

        rep1_statuses_count = rep1.deal_count_by_status()
        rep2_statuses_count = rep2.deal_count_by_status()

        return f"""
        Performance comparison:
        
        {rep1.name} ({rep1.role}, {rep1.region}):
        - Closed Won deals: {rep1_statuses_count.get("Closed Won", 0)} of {len(rep1.deals)}
        - Closed Won value: {rep1.get_deals_value_by_status("Closed Won"):,.2f}
        - Win Rate: {rep1.win_rate():.1f}%
        - Clients: {len(rep1.clients)}
        
        {rep2.name} ({rep2.role}, {rep2.region}):
        - Closed Won deals: {rep2_statuses_count.get("Closed Won", 0)} of {len(rep2.deals)}
        - Closed Won value: {rep2.get_deals_value_by_status("Closed Won"):,.2f}
        - Win Rate: {rep2.win_rate():.1f}%
        - Clients: {len(rep2.clients)}
        """

    def get_tools(self) -> List[Tool]:
        return [
            Tool(
                name="get_rep_performance",
                description="Get performance metrics for a spesific sales representative",
                func=self.get_rep_performance,
                args_schema=ToolSchema_RepName,
            ),
            Tool(
                name="compare_reps",
                description="Compare performance metrics between two sales representatives",
                func=self.compare_reps,
                args_schema=ToolSchema_CompareReps,
            )
        ]
