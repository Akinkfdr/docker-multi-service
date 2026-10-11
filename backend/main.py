import os
from minio import Minio
import psycopg2
import redis
from io import BytesIO
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Backend is running"
    }


@app.get("/db-check")
def db_check():
    connection = psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"]
    )

    connection.close()

    return {
        "database": "connected"
    }


@app.get("/redis-check")
def redis_check():
    client = redis.Redis(
        host=os.environ["REDIS_HOST"],
        port=os.environ["REDIS_PORT"],
        decode_responses=True
    )

    client.set("test-key", "hello-redis")
    value = client.get("test-key")

    return {
        "redis": "connected",
        "value": value
    }

@app.get("/minio-check")
def minio_check():
    client = Minio(
        os.environ["MINIO_ENDPOINT"],
        access_key=os.environ["MINIO_ACCESS_KEY"],
        secret_key=os.environ["MINIO_SECRET_KEY"],
        secure=False
    )

    bucket_name = os.environ["MINIO_BUCKET"]

    exists = client.bucket_exists(bucket_name)

    return {
        "minio": "connected",
        "bucket": bucket_name,
        "bucket_exists": exists
    }

@app.get("/minio-upload-test")
def minio_upload_test():
    client = Minio(
        os.environ["MINIO_ENDPOINT"],
        access_key=os.environ["MINIO_ACCESS_KEY"],
        secret_key=os.environ["MINIO_SECRET_KEY"],
        secure=False
    )

    bucket_name = os.environ["MINIO_BUCKET"]

    data = b"Hello from FastAPI and MinIO!"
    data_stream = BytesIO(data)

    client.put_object(
        bucket_name=bucket_name,
        object_name="hello.txt",
        data=data_stream,
        length=len(data),
        content_type="text/plain"
    )

    return {
        "uploaded": True,
        "object": "hello.txt"
    }

@app.get("/minio-read-test")
def minio_read_test():
    client = Minio(
        os.environ["MINIO_ENDPOINT"],
        access_key=os.environ["MINIO_ACCESS_KEY"],
        secret_key=os.environ["MINIO_SECRET_KEY"],
        secure=False
    )

    bucket_name = os.environ["MINIO_BUCKET"]

    response = client.get_object(
        bucket_name,
        "hello.txt"
    )

    content = response.read().decode("utf-8")

    response.close()
    response.release_conn()

    return {
        "object": "hello.txt",
        "content": content
    }