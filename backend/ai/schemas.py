from typing import Optional
from pydantic import BaseModel, Field


class QueryResponse(BaseModel):
    answer: str


class QueryRequest(BaseModel):
    message: str = Field(..., description="The question to ask the AI model")
    # context: str = Field(..., description="The context for the AI model to consider when answering the question")
    rep_context_id: Optional[int] = Field(..., description="The ID of the sales rep context to use")


# Define schema models for tool arguments
class ToolSchema_RepName(BaseModel):
    rep_name: str = Field(..., description="The name of the sales rep")


class ToolSchema_CompareReps(BaseModel):
    rep1_name: str = Field(..., description="The name of the first sales rep to compare")
    rep2_name: str = Field(..., description="The name of the second sales rep to compare")


class ToolSchema_RepDealStatus(BaseModel):
    rep_name: str = Field(..., description="The name of the sales rep")
    status: str = Field(..., description="The deal status to count (e.g., 'Closed Won', 'Closed Lost', 'In Progress')")
