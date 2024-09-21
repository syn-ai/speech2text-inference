#! /bin/bash

if [ -f in/audio_data.wav ]; then
    bash scripts/convert_ffmpeg.sh ./in/audio_data.wav
fi

if [ -f in/audio_data.wav ]; then
    ./main -m ggml-base.en.bin -f out/output.wav -t 32 -di -otxt out/output.txt
fi
