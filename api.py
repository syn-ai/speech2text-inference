import base64
import subprocess
from pathlib import Path
import os
import uvicorn
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from whisper import run_whisper

from utilities.data_models import TranscriptionRequest
from utilities.endpoint_configs import EndpointConfigManager

manager = EndpointConfigManager()
config = manager.stt

path = Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


run_script = Path("scripts/run_whisper.sh")

run_script.chmod(0o777)


@app.post(f"{manager.version}{config.endpoint}")
def transcribe(request: TranscriptionRequest):
    # Specify the URL to which the request will be sent
    url = 'http://0.0.0.0:7098/tts'

    # Specify the path to the file you want to upload
    file_path = 'in/input.wav'  
    output_path = 'in/output.wav'
    filepath = Path(file_path)
    file_path = filepath.write_bytes(request.data)
    outpath = Path(output_path)

    try:
        response = run_whisper('./main', filepath, 'ggml-base.en.bin')
        # Check if the request was successful
        data = base64.b64decode(outpath.read_bytes()).decode("utf-8")
        print(data)
        return data
    except Exception as e:
        raise e
    return response.json()



if __name__ == "__main__":
    uvicorn.run("api:app", host=config.host, port=int(config.port), reload=True)
