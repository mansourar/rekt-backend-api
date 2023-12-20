import os

import boto3

from app.internal.helpers.components.environment import Environment

GLOBAL_ENV = Environment()

BUCKETS = [
    "test-bucket"
]


def get_bucket_name(bucket):
    bucket_name = f"{GLOBAL_ENV.ENV}-rekt-{bucket}"
    return bucket_name


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

    def verify_buckets(self):
        try:
            for bucket in BUCKETS:
                self.client.head_bucket(Bucket=get_bucket_name(bucket))
        except Exception as exc:
            return False, str(exc)
        return True, None

    def delete_object(self, bucket: str, key: str) -> (bool, str):
        try:
            self.client.delete_object(Bucket=get_bucket_name(bucket), Key=key)
        except Exception as exc:
            return False, f"{exc}"
        return True, ""

    def delete_all_objects(self, bucket: str, prefix: str) -> (bool, str):
        try:
            objects = self.client.list_objects(Bucket=get_bucket_name(bucket), Prefix=f"{prefix}/")
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
            result = self.client.get_object(Bucket=get_bucket_name(bucket), Key=key)
            if len(result) == 0:
                return False, f"object in bucket {get_bucket_name(bucket)} with {key} is empty"
        except Exception as exc:
            return False, f"failed to get object in bucket {get_bucket_name(bucket)} with {key}: {exc}"
        return True, result

    def put_object(self, bucket: str, key: str, body) -> (bool, str):
        try:
            self.client.put_object(
                Bucket=get_bucket_name(bucket), Body=body, Key=key, ContentType=self.content_type
            )
            return True, f"{get_bucket_name(bucket)}/{key}"
        except Exception as exc:
            return False, f"failed to put object contents in bucket {get_bucket_name(bucket)} with {key}: {exc}"
