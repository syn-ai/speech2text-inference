FROM nvcr.io/nvidia/tritonserver:24.01-py3
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
WORKDIR /app
COPY . /app

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y libbz2-dev libcurses-ocaml-dev lzma-dev python3-tk libsqlite3-dev python3 python3-venv python3-pip python3-dev python-is-python3 curl wget nano ffmpeg git git-lfs build-essential -s

