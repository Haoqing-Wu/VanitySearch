from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import File, UploadFile
from fastapi import FastAPI, File, UploadFile, APIRouter, Depends, Request, status
from minio import Minio
from typing_extensions import Annotated
from datetime import timedelta
import random,json
import urllib.request
import time
import subprocess


app = FastAPI(title="vanity_search",version='0.0.1')


origins = ["*"]
app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"])  

class InputData(BaseModel):
    addr: str 


def getRandom(randomlength=10):
    digits = "0123456789"
    ascii_letters = "abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    str_list = [random.choice(digits + ascii_letters) for i in range(randomlength)]
    random_str = ''.join(str_list)
    print(random_str)
    return random_str

def upload_file(source_file):
    client = Minio("124.193.167.71:19000",
        access_key="zGVaTSxqrhz6bPuVfSls",
        secret_key="SvMqa7zY1xJAw2dxKUZtKKsvECOQu9cExYjYXcXx",
        secure=False
    )

    bucket_name = "agicoin"
    destination_file = 'output_' + getRandom(20) + '.' + source_file.split('.')[-1]
    
    # Make the bucket if it doesn't exist.
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
        print("Created bucket", bucket_name)
    else:
        print("Bucket", bucket_name, "already exists")

    # Upload the file, renaming it in the process
    result = client.fput_object(
        bucket_name, destination_file, source_file,
    )
    print(
        "created {0} object; etag: {1}, version-id: {2}".format(
            result.object_name, result.etag, result.version_id,
        ),
    )
    url = client.get_presigned_url(
        "GET",
        bucket_name,
        result.object_name,
        expires=timedelta(minutes=30),
    )
    print(
        source_file, "successfully uploaded as object",
        destination_file, "to bucket", bucket_name,
    )
    print("url:", url)
    return url

@app.post("/aigic")
def aigic(inputdata: InputData):
    print('+++++++++++++++++++++++++++++++++++++++++++++++++')
    print('1. Input address:', inputdata.addr)

    print('2. Inferring ... ')
    t1 = time.time()
    output = subprocess.check_output(['usr/bin/VanitySearch', '-stop', '-gpu', inputdata.addr]).decode().strip()
    print('5. Output Info:', output)
    print('4. Inference time cost:', time.time() - t1)

    ret = {
    "output": output
    }
    outfile = "output.json"
    with open(outfile, 'w') as fw:
        fw.write(json.dumps(ret))
    
    return {
    "code": 200,
    "msg": "success",
    "content": ret 
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=8090)