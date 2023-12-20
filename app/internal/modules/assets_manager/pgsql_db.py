from sqlalchemy import text

from app.exceptions import AssetsRecordsQueryException


async def list_assets(psql_session, changelist):
    try:
        query_params = {"cl": changelist}
        query = text(
            "select * from assets "
            "where changelist >= :cl"
        )
        result = psql_session.execute(query, params=query_params)
        res_array = []
        for row in result:
            row = row._asdict()
            obj = {
                "id": row["asset_id"],
                "name": row["asset_name"],
                "type": row["asset_type"],
                "path": row["s3_location"],
                "cl": row["changelist"],
                "checksum": row["checksum"]
            }
            res_array.append(obj)
        return {"assets": res_array}
    except Exception as exc:
        raise AssetsRecordsQueryException(f"failed to query for assets records: {str(exc)}")
