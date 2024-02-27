#!/bin/bash

INPUT=$1

if [ -f output/output.wav ]; then
    rm output/input.wav
fi

export CUDA_VISIBLE_DEVICE=3

ffmpeg -i $INPUT -af "pan=stereo|c0=c0|c1=c1" -ar 16000 -ac 2 -acodec pcm_s16le output/input.wav -y

