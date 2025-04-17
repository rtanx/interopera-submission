from pydantic import BaseModel, Field


class QueryResult(BaseModel):
    answer: str


# Define schema models for tool arguments
class ToolSchema_RepName(BaseModel):
    rep_name: str = Field(..., description="The name of the sales rep")


class ToolSchema_CompareReps(BaseModel):
    rep1_name: str = Field(..., description="The name of the first sales rep to compare")
    rep2_name: str = Field(..., description="The name of the second sales rep to compare")


class ToolSchema_RepDealStatus(BaseModel):
    rep_name: str = Field(..., description="The name of the sales rep")
    status: str = Field(..., description="The deal status to count (e.g., 'Closed Won', 'Closed Lost', 'In Progress')")
