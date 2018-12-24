#!/bin/python

import os
import argparse
import numpy as np
import struct
import webrtcvad

from scipy.io import wavfile
train_audio_path = "/home/ricardo/Documents/TFM/codigo/audio/ass.wav"
# filename = 'yes/0a7c2a8d_nohash_0.wav'


def get_args():
    desc = "Split audio.wav when nobody is speaking"
    epilog = """
             this file is make automatic audio samples split.

             Examples:
             python VAD_plit.py -f Path/to/audio.wav
             """
    parser = argparse.ArgumentParser(description=desc, epilog=epilog,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('-i', '--input',
                        help='name of audio you want to split',
                        required=True)

    parser.add_argument('-o', '--output',
                        help='path to output example /path/to/output/',
                        required=True)
    parser.add_argument('-a', '--aggressive',
                        help='level of aggresivisness of the split',
                        required=False)
    ret = parser.parse_args()
    return ret


def get_segments(samples, raw_samples, sample_rate, samples_per_window,
                 bytes_per_sample):
    segments = []
    for start in np.arange(0, len(samples), samples_per_window):
        try:
            stop = min(start + samples_per_window, len(samples))
            is_speech = vad.is_speech(
                    raw_samples[start * bytes_per_sample: stop *
                                bytes_per_sample],
                    sample_rate=sample_rate)

            segments.append(dict(
                                 start=start, stop=stop, is_speech=is_speech))
        except Exception as e:
            print(f'error in {e}:  start {start} : stop {stop}')
    return segments


def audio_spliter(segments, output_path):
    silencio = 0
    voz = 0
    count = 0
    lista = []
    primera = 0
    for segment in segments:
        if segment['is_speech']:
            silencio = 0
            if voz == 0:
                start = segment['start']
            stop = segment['stop']
            lista.append((segment['start'], segment['stop']))
            primera = 1
            voz += 1
        else:
            if silencio >= 1:
                if primera and stop - start > 10000:
                    # speech_samples = samples[start:stop]
                    speech_samples = np.concatenate(
                            [samples[j[0]:j[1]] for j in lista])
                    wavfile.write("{}out-{}-{}.wav".format(
                            output_path, start, stop), sample_rate,
                            speech_samples)
                    count += 1
                    lista = []
                voz = 0
                primera = 0
            silencio += 1
    if stop - start > 10000 and voz > 0:
        print(stop - start)
        speech_samples = np.concatenate([samples[j[0]:j[1]] for j in lista])
        wavfile.write("{}out-{}-{}.wav".format(output_path, start, stop),
                      sample_rate, speech_samples)


if __name__ == '__main__':
    args = get_args()
    sample_rate, samples = wavfile.read(os.path.dirname(
                                        os.path.abspath(__file__)) + args.input)
    vad = webrtcvad.Vad()
    if args.aggressive:
        vad.set_mode(int(args.aggressive))
    else:
        vad.set_mode(3)
    # convert samples to raw 16 bit per sample stream needed by webrtcvad
    raw_samples = struct.pack("%dh" % len(samples), *samples)
    window_duration = 0.02  # duration in seconds
    samples_per_window = int(window_duration * sample_rate + 0.5)
    bytes_per_sample = 2
    segments = get_segments(samples, raw_samples, sample_rate,
                            samples_per_window, bytes_per_sample)
    audio_spliter(segments, args.output)


# speech_samples = np.concatenate(
# [samples[segment['start']:segment['stop']]
# for segment in segments if segment['is_speech']])
# wavfile.write("jojojojojo.wav", sample_rate, speech_samples)
