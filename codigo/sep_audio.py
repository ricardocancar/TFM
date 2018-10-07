#!/usr/bin/python3
# -*- coding: utf-8 -*-
# $File: sep_audio.py
# $Date: Tue Jun 10 15:18:40 2014 +0800
# $Author: Ricardo cancar <ricardocancar[at]gmail[dot]com>
import os
import argparse
#ffmpeg -i somefile.mp3 -f segment -segment_time 3 -c copy out%03d.mp3

def get_args():
    desc = "Split Audio File Command Line Tool"
    epilog = """
the wav file will be split in several file the amount split will depent on the duration of the file and the length you want to split this file

Examples:
    Train (enroll a list of person named person*, and mary, with wav files under corresponding directories):
    ./speaker-recognition.py -t enroll -i "./bob/ ./mary/ ./person*" -m model.out

    Predict (predict the speaker of all wav files):
    ./speaker-recognition.py -t predict -i "./*.wav" -m model.out
"""
    parser = argparse.ArgumentParser(description=desc,epilog=epilog,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-i', '--input',
                       help='Input Files(to split)',
                       required=True)

    parser.add_argument('-l', '--len',
                       help='Lenght of the Split',
                       required=False)

    ret = parser.parse_args()
    return ret

def spliter(audio, length = 1):
  if  not os.path.exists("tmp"):
      os.system("mkdir tmp")
  os.system("ffmpeg -i {} -f segment -segment_time {} -c copy ./predict/out%03d.wav".format(audio,length))


if __name__ == "__main__":
  args = get_args()
  if args.len != None:
    spliter(args.input,args.len)
  else:
    spliter(args.input)


