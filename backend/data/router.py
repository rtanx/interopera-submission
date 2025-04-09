from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_data():
    """
    Returns dummy data.
    """
    dummy_data = [
        {"id": 1, "name": "John Doe"},
        {"id": 2, "name": "Jane Smith"}
    ]
    return dummy_data
