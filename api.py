import base64
from pathlib import Path
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from whisper import run_whisper

from utilities.data_models import TranscriptionRequest
from utilities.endpoint_configs import EndpointConfigManager

manager = EndpointConfigManager()
config = manager.speech2text

path = Path

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


@app.post(f"{config.endpoint}")
def transcribe(request: TranscriptionRequest):
    # Specify the path to the file you want to upload
    if not request.data:
        raise ValueError("No data provided")
    input_path = "in/output.wav"
    output_path = "in/output.wav"
    filepath = Path(input_path)
    filepath.write_bytes(base64.b64decode(request.data.encode("utf-8")))
    outpath = Path(output_path)

    try:
        response = run_whisper(whisper_bin, input_path, whisper_model)
        # Check if the request was successful
        data = (
            base64.b64encode(outpath.read_bytes()).decode("utf-8")
            if outpath.exists()
            else outpath.read_bytes()
        )
        print(data)
        return data
    except Exception as e:
        raise e
    return response.json()


if __name__ == "__main__":
    uvicorn.run("api:app", host=config.host, port=int(config.port), reload=True)
