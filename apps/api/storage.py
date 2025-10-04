import os
from urllib.parse import urlparse
from minio import Minio
from minio.error import S3Error

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "admin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "adminadmin")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "photos")

def _make_client() -> Minio:
    parsed = urlparse(MINIO_ENDPOINT)
    secure = parsed.scheme == "https"
    netloc = parsed.netloc or parsed.path  # in case someone sets just host:port
    return Minio(
        netloc,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=secure,
    )

client = _make_client()

# ensure bucket exists
found = client.bucket_exists(MINIO_BUCKET)
if not found:
    client.make_bucket(MINIO_BUCKET)

def put_object(object_name: str, data, length: int, content_type: str | None = None):
    """
    Uploads an object to MINIO_BUCKET.
    data: a file-like object, opened in binary.
    length: number of bytes to upload.
    """
    extra_headers = {"Content-Type": content_type} if content_type else None
    return client.put_object(
        MINIO_BUCKET,
        object_name,
        data,
        length,
        content_type=content_type,
        metadata=None,
        sse=None,
        tags=None,
        retention=None,
        part_size=5 * 1024 * 1024,
    )
