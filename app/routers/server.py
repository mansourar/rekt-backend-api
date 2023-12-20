import fastapi
from fastapi.security import HTTPBasic

router = fastapi.APIRouter()
security = HTTPBasic()


@router.get("/ping")
async def root():
    return {"code": 200, "message": "pong"}
