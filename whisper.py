import argparse
import subprocess
from pathlib import Path
from convert_file import convert_to_wav

subprocess.run(["pip", "install", "loguru", "-q"], check=True)

from loguru import logger

path = Path


def run_whisper(
    whisper_bin="./main",
    file_path="in/input.wav",
    model_path="ggml-base.en.bin",
):
    file_path = path.cwd() / file_path
    model_path = path.cwd() / model_path
    if os.path.exists("in/output.wav"):
        os.remove("in/output.wav")
    try:
        convert_to_wav(file_path)
    except Exception as e:
        logger.error(e)
        return e

    try:
        result = subprocess.run(
            [f"{whisper_bin}", "-m", f"{model_path}", "-f", f"in/output.wav", "--otxt", f"out/output.txt"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        logger.debug(result.stdout.decode("utf-8"))
        print(result.stdout.decode("utf-8"))
        return result.stdout.decode("utf-8")
    except subprocess.CalledProcessError as error:
        logger.error(error)
        return error
    except RuntimeError as error:
        logger.error(error)
        return error


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file_path", default="in/jfk.wav", type=str, required=False
    )
    parser.add_argument(
        "-m",
        "--model_path",
        default="ggml-base.en.bin",
        type=str,
        required=False,
    )
    parser.add_argument("-w", "--whisper_bin", default="./main", type=str)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    run_whisper(**vars(args))
