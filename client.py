import json
import base64
import argparse
import requests
from loguru import logger
from pathlib import Path
import os
from pydantic import BaseModel
from utilities.data_models import TranscriptionRequest
from utilities.endpoint_configs import EndpointConfigManager

manager = EndpointConfigManager()

config = manager.stt


def transcribe(
    file_path="in/test.wav",
    temperature="0.0",
    temperature_inc="0.2",
    response_format="json",
):
    with open(file_path, "rb") as file:
        data = base64.b64encode(file.read()).decode("utf-8")
    # normal

    transcription_request = TranscriptionRequest(
        data=data
    ).model_dump()

    resp = requests.post(
        url=f"http://0.0.0.0:7098{manager.version}{config.endpoint}",
        json=transcription_request,
        timeout=6000,
    )
    if resp.status_code == 200:
        return resp.json()
    logger.error(resp.status_code)

    return resp


if __name__ == "__main__":
    transcribe()
