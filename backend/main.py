from fastapi import Depends, FastAPI

from .routers import ai, data

app = FastAPI()

app.include_router(data.router, prefix="/api/data", tags=["data"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])


@app.get("/", tags=["root"])
async def read_root():
    """
    Root endpoint.
    """
    return {"message": "Hello InterOpera!"}
