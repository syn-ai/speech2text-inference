import base64
from pathlib import Path
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from whisper import run_whisper
import os
import subprocess
import time
from utilities.data_models import TranscriptionComplete
from utilities.endpoint_configs import EndpointConfigManager

manager = EndpointConfigManager()
config = manager.speech2text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

whisper_model = "ggml-base.en.bin"
whisper_bin = "./main"

run_script = Path("scripts/run_whisper.sh")

run_script.chmod(0o777)


@app.post(f"/speech2text")
def transcribe(request: TranscriptionComplete):
    # Specify the path to the file you want to upload
    if not request.audio:
        raise ValueError("No data provided")
    input_folder = Path("in")
    output_folder = Path("out")
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
    input_path = input_folder / "audio_data.wav"
    output_text_path = output_folder / "output.wav.txt"
    converted_path = output_folder / "output.wav"
    input_path.write_bytes(base64.b64decode(request.audio.encode("utf-8")))
    command = ["bash", "./scripts/run_whisper.sh"]
    try:
        subprocess.run(command, check=True)
        while not output_text_path.exists():
            time.sleep(0.1)
        with open(output_text_path, "r") as file:
            text = file.read()        
    except Exception as e:
        return {"error": str(e)}
    output_text_path.unlink()
    input_path.unlink()
    converted_path.unlink()
    
    return text


if __name__ == "__main__":
    uvicorn.run("api:app", host=config.host, port=int(config.port))
