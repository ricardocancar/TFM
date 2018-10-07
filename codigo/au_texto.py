import speech_recognition as sr
import argparse
import os
import itertools
import glob
import re
def get_args():
   desc = "is a speech to text script"
   epilog = "-a directory of python files audio input -o name_file.txt both args are require"

   parser = argparse.ArgumentParser(description=desc,epilog=epilog,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
   parser.add_argument('-a', '--audio',
                       help='audio file input to transform in text',
                       required=True)

   parser.add_argument('-o', '--out',
                       help ='name of file output',
                       required = False)
   ret = parser.parse_args()
   return ret

def audios(input_dirs):
    input_dirs = [os.path.expanduser(k) for k in input_dirs.strip().split()] #iterator
    dirs = itertools.chain(*(glob.glob(d) for d in input_dirs)) # generator 
    dirs = [d for d in dirs if os.path.isdir(d)]
    if len(dirs) == 0:
        print("No valid directory found!")
        sys.exit(1)
    for d in dirs:
        wavs = glob.glob(d + '/*.wav')
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


def audio_text(salida, r, audio):
   salida = salida.split('/')[-1]
   salida = re.match(r"([a-z]+)([0-9:]+)", salida, re.I).groups()
   print(salida)
   with open("./text/{}.txt".format(salida[0]),"a") as f:
       f.write(salida[1] + '\n\n')
       f.write(r.recognize_google(audio,language="es").encode('utf-8') + '\n\n') # ca-ES catalan
  


if __name__=='__main__':
    args = get_args()
    wavs=audios(args.audio)
    for wav in wavs:
       r, audio = read_wav(wav)
       audio_text(wav, r, audio)
