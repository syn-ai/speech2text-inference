FROM python:3.10-slim-bullseye
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
WORKDIR /app
COPY . /app

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y ffmpeg libgomp1 libgcc-10-dev libbz2-dev libcurses-ocaml-dev lzma-dev python3-tk libsqlite3-dev python3 python3-venv python3-pip python3-dev python-is-python3 curl wget nano ffmpeg git git-lfs build-essential -s

RUN pip install --upgrade pip

RUN pip install setuptools wheel gnureadline

RUN pip install -r requirements.txt

RUN bash install_whisper.sh

CMD ["python","api.py"]
