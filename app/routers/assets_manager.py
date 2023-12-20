import fastapi
from fastapi.security import HTTPBasic
from starlette import status

from app.internal.database.postgres.pgsql_helper import PgsqlReader
from app.internal.modules.assets_manager import pgsql_db

router = fastapi.APIRouter()
security = HTTPBasic()


@router.get("/list_assets", status_code=status.HTTP_200_OK)
async def list_assets(
        cl: int
):
    with PgsqlReader.SESSION_MAKER() as psql_session:
        result = await pgsql_db.list_assets(
            psql_session=psql_session,
            changelist=cl
        )
        return result


@router.post("/upload")
async def upload_asset():
    pass


@router.post("/download")
async def download_asset():
    pass
