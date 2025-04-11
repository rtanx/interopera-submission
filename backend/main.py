from fastapi import Depends, FastAPI

from .data import router as data_router
from .ai import router as ai_router

app = FastAPI()

app.include_router(data_router.router, prefix="/api/sales-reps", tags=["sales-reps"])
app.include_router(ai_router.router, prefix="/api/ai", tags=["ai"])


@app.get("/", tags=["root"])
async def read_root():
    """
    Root endpoint.
    """
    return {"message": "Hello InterOpera!"}
