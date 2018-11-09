import speech_recognition as sr
import argparse
import os
import itertools
import glob
import re
import datetime
import sys
import pandas as pd
import numpy


def get_args():
    desc = "is a speech to text script"
    epilog = ("-a directory of python files audio input -o name_file.txt both"
              "args are require")

    parser = argparse.ArgumentParser(description=desc, epilog=epilog,
                                     formatter_class=argparse
                                     .RawDescriptionHelpFormatter)
    parser.add_argument('-a', '--audio',
                        help='path to dir audio files to transform in text',
                        required=True)

    parser.add_argument('-o', '--out',
                        help='name of file output',
                        required=False)
    ret = parser.parse_args()
    return ret


def audios(input_dirs):
    input_dirs = [os.path.expanduser(k) for k in input_dirs.strip().split()]
    # iterator
    dirs = itertools.chain(*(glob.glob(d) for d in input_dirs))
    # generator
    dirs = [d for d in dirs if os.path.isdir(d)]
    if len(dirs) == 0:
        print("No valid directory found!")
        sys.exit(1)
    for d in dirs:
        wavs = glob.glob(d + '/*.wav')
        if len(wavs) > 1:
            wavs = sorted(wavs)
        if len(wavs) == 0:
            print("No wav file found in {0}".format(d))
            sys.exit(1)
        else:
            return wavs


def read_wav(audio):
    r = sr.Recognizer()
    telediario = sr.AudioFile(audio)
    with telediario as source:
        audio = r.record(source)
    return r, audio


def audio_text(salida, r, audio, df):
    salida = salida.split('/')[-1]
    salida = re.match(r"(\w+)(-)([0-9.]+)(-)([0-9]+)", salida, re.I).groups()
    start = float(salida[2])  # /16000
    end = float(salida[4])  # /16000
    index_list = df.index.values
    true_table = (df['start'] + 1 > start) & (df['start'] - 1 < end)
    for i in range(len(index_list)):
        if numpy.bool(true_table[index_list[i]]) is True:
            last_index = index_list[i]
    try:
        dictio = {'label': df.loc[last_index]['label'],
                  'start-end': f'{start}-{end}',
                  'text': str(r.recognize_google(audio, language="es"))}
        row = pd.Series(dictio)
#        df['text'][(df['start'] + 1 > start) & (df['start'] - 1 < end)] \
#            = str(r.recognize_google(audio, language="es"))
    except sr.UnknownValueError as e:
            print(("couldn't do speech to text due lack of "
                   f"data in audio: {salida[0]} time: {start}-{end}"))
            dictio = {'label': df.loc[last_index]['label'],
                      'start-end': f'{start}-{end}',
                      'text': ''}
            row = pd.Series(dictio)
#    start1 = str(datetime.timedelta(seconds=start/16000))
#    end1 = str(datetime.timedelta(seconds=end/16000))
#   df['start-date-time'][(df['start'] + 1 > start) & (df['start'] - 1 < end)]\
#        = start1
#    df['end-date-time'][(df['start'] + 1 > start) & (df['start'] - 1 < end)]\
#        = end1
    return row
#    df.to_csv('exit.csv')


if __name__ == '__main__':
    args = get_args()
    wavs = audios(args.audio)
    for wav in wavs:
        r, audio = read_wav(wav)
        audio_text(wav, r, audio)
