import boto3
import  mimetypes
from io import BytesIO
from typing import Union

from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse, FileResponse

app = FastAPI()


@app.post("/upload")
def upload(file: UploadFile):
    s3 = boto3.client("s3")
    response = s3.upload_fileobj(file.file, "lab-cloud-luis", file.filename)
    return JSONResponse(content={"message": "File uploaded successfully", "filename": file.filename}, status_code=200)


@app.get("/download")
def download(filename: str):
    s3 = boto3.client("s3")
    s3.download_file("lab-cloud-luis", filename, filename)
    return FileResponse(filename, headers={"Content-Disposition": f"attachment; filename={filename}"})

@app.get("/list")
def list():
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(Bucket="lab-cloud-luis")
    object_list = [obj['Key'] for obj in response.get('Contents', [])]
    return JSONResponse(content=object_list, status_code=200)