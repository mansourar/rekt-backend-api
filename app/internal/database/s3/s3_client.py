import os

import boto3

from app.internal.helpers.components.environment import Environment

GLOBAL_ENV = Environment()

MASTER_BUCKET = GLOBAL_ENV.ENV

FOLDERS = [
    "assets/",
    "others/",
    "others1/",
    "others2/"
]


class S3Client:

    def __init__(
            self,
            content_type: str = "binary/octet-stream"
    ):
        self.env = GLOBAL_ENV.ENV
        self.content_type = content_type
        if GLOBAL_ENV.is_local:
            self.client = boto3.client(
                "s3",
                "eu-west-1",
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                endpoint_url=f"{os.getenv('S3_ENDPOINT', 'http://localhost:9000')}",
            )
        else:
            self.client = boto3.client("s3", "eu-west-1")

    def environment_bucket_check(self):

        response, error = self.create_bucket(MASTER_BUCKET)
        if error:
            return False, error

        response, error = self.create_folders(MASTER_BUCKET)
        if error:
            return False, error

        return True, None

    def bucket_exists(self, bucket):
        try:
            self.client.head_bucket(Bucket=bucket)
            return True, None
        except Exception as exc:
            return False, str(exc)

    def folder_exits(self, bucket, folder):
        try:
            self.client.head_object(Bucket=bucket, Key=folder)
            return True, None
        except Exception as exc:
            return False, str(exc)

    def create_bucket(self, bucket_name: str):
        try:
            response, error = self.bucket_exists(bucket_name)
            if not response:
                self.client.create_bucket(Bucket=bucket_name)
        except Exception as exc:
            return False, str(exc)
        return True, None

    def create_folders(self, bucket_name: str):
        try:
            for folder in FOLDERS:
                response, error = self.folder_exits(bucket_name, folder)
                if error:
                    print(folder)
                    self.client.put_object(Bucket=MASTER_BUCKET, Key=folder)
        except Exception as exc:
            return False, f"failed to put object contents in bucket {MASTER_BUCKET} : {str(exc)}"

        return True, None

    def list_bucket(self, dir_filter: str):
        response = self.client.list_objects_v2(Bucket=MASTER_BUCKET)
        dir_list = []
        for obj in response.get('Contents', []):
            if str(obj["Key"]).startswith(f"{dir_filter}"):
                dir_list.append({
                    "key": obj['Key'],
                    "lastModified": obj['LastModified'].strftime('%Y-%m-%d %H:%M:%S %Z'),
                    "bytesSize": obj['Size'],
                })
        return {
            "dir": dir_list
        }

    def delete_object(self, bucket: str, key: str) -> (bool, str):
        try:
            self.client.delete_object(Bucket=bucket, Key=key)
        except Exception as exc:
            return False, f"{exc}"
        return True, ""

    def delete_all_objects(self, bucket: str, prefix: str) -> (bool, str):
        try:
            objects = self.client.list_objects(Bucket=bucket, Prefix=f"{prefix}/")
        except Exception as exc:
            return (
                False,
                f"failed to list objects in {self.bucket} at {prefix}/ for deletion: {exc}",
            )

        errors = {}
        for content in objects.get("Contents", []):
            key = content.get("Key")
            result, msg = self.delete_object(key)
            if not result:
                errors[key] = msg

        if len(errors) > 0:
            error_msgs = "\n".join(f"{key} {value}" for key, value in errors.items())
            return (
                False,
                f"could not delete all objects in {self.bucket} at {prefix}/: {error_msgs}",
            )

        return True, ""

    def get_object(self, bucket: str, key: str) -> (bool, str):
        try:
            result = self.client.get_object(Bucket=bucket, Key=key)
            if len(result) == 0:
                return False, f"object in bucket {bucket} with {key} is empty"
        except Exception as exc:
            return False, f"failed to get object in bucket {bucket} with {key}: {exc}"
        return True, result

    def put_object(self, bucket: str, key: str, body) -> (bool, str):
        try:
            self.client.put_object(
                Bucket=bucket, Body=body, Key=key, ContentType=self.content_type
            )
            return True, None
        except Exception as exc:
            return False, f"failed to put object contents in bucket {bucket} with {key}: {exc}"
