from app.internal.database.s3.s3_client import S3Client


async def assets_list(dir_filter: str):
    s3_client = S3Client()
    return s3_client.list_bucket(dir_filter)


async def assets_download(file_name: str):
    pass


async def asset_upload(file_name: str):
    pass
