#! /bin/bash

if [ -f output/input.wav ]; then
    ./main -m ggml-base.en.bin -f output/input.wav -t 32 -di -otxt    
fi
