import re
import pandas as pd
import numpy as np
import argparse
import shutil
from scipy.io import wavfile

def get_args():
    desc = "order the classifications maked by the speaker reconigtions on time line"
    epilog = """
             extrac the audio parts to be analice in future.

             Examples:
             python VAD_plit.py -f Path/to/audio.wav 
             """
    parser = argparse.ArgumentParser(description=desc,epilog=epilog,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-i', '--input',
                       help='name of audio you want to split',
                       required=True)

    ret = parser.parse_args()
    return ret


def sort_classifications():
    df = pd.read_csv("predictions.csv")
    # df['new'] = pd.Series(np.random.randn(len(df['file'])), index=df.index)
    for i in range(len(df)):
        #print(df['file'][i].split('/')[-1])
        start_end = re.findall(r'[0-9]*-[0-9]*',
                                 df['file'][i].split('/')[-1])
        #print((start_end[0].replace('-',''), start_end[1].replace('-','')))
        df.loc[i,'start'] = int(start_end[0].replace('-',''))
        df.loc[i,'end'] = int(start_end[1].replace('-','')) 
        #df.loc[i,'new'] = re.findall(r'[0-9]*:[0-9]*:[0-9]+',
        #                             df['file'][i].split('/')[-1])[0]
        df.loc[i,'file'] = re.findall(r'(?<=host)[/\w+/]+',
                                      df['file'][i])[0][:-11]
        #df.loc[i,'file'] = re.findall(r'(?<=host)[/\w+/]+',
        #                              df['file'][i])[0][:-3]
    df = df.sort_values(by=['start'])
    df.to_csv('sorted_prediction.csv')
    return df

def write(df,i,index_list,count,start,end, label, eol = None):
   speech_samples =  samples[int(start):int(end)] 
   wavfile.write("{}audio_to_txt/{}-{}-{}.wav".format(df['file'][i],label,start,
                                                                       end), sample_rate, speech_samples)
   if eol != 'EOL':
      start = df.loc[index_list[count + 1],'start']
      end = df.loc[index_list[count + 1],'end']
      label = df.loc[index_list[count + 1],'label']
      return  start, end, label

def write_audio_classification(df):
    begin = True
    index_list = df.index.tolist()
    index_list.append('EOL')
    count=0
    if index_list[0] != 'EOL':
        for i in index_list[:-1]:
            if begin:
                label = df.loc[i,'label']
                start = df.loc[i,'start']
                end = df.loc[i,'end']
                begin = False
            if index_list[count + 1] == 'EOL':
                write(df,i,index_list,count,start,end, label, 'EOL')
            #print(df.loc[index_list[count],'label'], df.loc[index_list[count+1],'label'])
            elif df.loc[index_list[count],'label'] == df.loc[index_list[count + 1],'label']:
                if df.loc[index_list[count + 1],'start'] - end > 32000:
                    # print(df.loc[index_list[count + 1],'start'] - end)
                    # if the politician take more tha 2 secons sice he finis to talk to start to talk again
                    # we split the prediction
                    start, end, label = write(df,i,index_list,count,start,end, label)
                else:
                    end = df.loc[index_list[count + 1],'end']
            elif df.loc[index_list[count],'label'] != df.loc[index_list[count + 1],'label']:
                start, end, label = write(df,i,index_list,count,start,end, label)
            count+=1

if __name__=='__main__':
    args = get_args()
    sample_rate, samples = wavfile.read(args.input)
    df = sort_classifications()
    write_audio_classification(df)

