#!/bin/bash

INPUT=$1

if [ -f out/output.wav ]; then
    rm out/output.wav
fi

export CUDA_VISIBLE_DEVICE=3

ffmpeg -i $INPUT -af "pan=stereo|c0=c0|c1=c1" -ar 16000 -ac 2 -acodec pcm_s16le out/output.wav -y

