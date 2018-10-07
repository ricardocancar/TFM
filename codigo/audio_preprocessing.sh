#!/bin/bash
##to improve
programname=$0

function usage {
    echo "usage: $programname [-n] [-f infile] [-o outfile]"
    echo "  -a      noise audio input to surpress"
    echo "  -f infile   specify input file infile"
    echo "  -o outfile  specify output file outfile"
    exit 1
}

# ffmpeg -i Pablo43.wav.wav -af "highpass=f=200, lowpass=f=3000" Pablo34.wav

sox noiseaud.wav -n noiseprof noise.prof

sox nnn.wav tmpaud-clean.wav noisered noise.prof 0.21

# ffmpeg -i i nput.wav -filter_complex "highpass=f=400,lowpass=f=1800" out2.wav

# ffmpeg -i i nput.wav -af "equalizer=f=1000:width_type=h:width=900:g=-10" output.wav

# ffmpeg -i i nput.wav -af "bandreject=f=1200:width_type=h:width=900:g=-10" output.wav

