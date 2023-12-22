from typing import Optional

import fastapi
from fastapi.security import HTTPBasic
from starlette import status

from app.internal.modules.assets_manager.redis_db import read_dir_cache, create_dir_cache
from app.internal.modules.assets_manager.storage_s3 import assets_list

router = fastapi.APIRouter()
security = HTTPBasic()

asset_dir_key = "assets_list"


@router.get("/list_assets", status_code=status.HTTP_200_OK)
async def list_assets(
        dir_filter: Optional[str] = "assets"
):
    response, error = await read_dir_cache(asset_dir_key)
    if error:
        response = await assets_list(dir_filter=dir_filter)
        await create_dir_cache(asset_dir_key, response)
    return response


@router.post("/upload")
async def upload_asset():
    pass


@router.post("/download")
async def download_asset():
    pass
