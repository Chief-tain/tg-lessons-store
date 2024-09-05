from miniopy_async import Minio
from shared.settings import S3_ENDPOINT, S3_ACCESS_KEY, S3_SECRET_KEY, S3_SECURE

client: Minio = Minio(
    endpoint=S3_ENDPOINT,
    access_key=S3_ACCESS_KEY,
    secret_key=S3_SECRET_KEY,
    secure=S3_SECURE,
)
