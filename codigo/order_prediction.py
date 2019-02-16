import re
import os
import glob
import pandas as pd
import sqlite3
from scipy.io import wavfile
import au_texto

DIR_INPUT = '/audio_start'

FILE_PATH = os.path.dirname(os.path.abspath(__file__))


def sort_classifications():
    name = au_texto.audios(f'.{DIR_INPUT}')
    # it work for only one file at time for now
    # name = name[0].split('/')[-1]
    name = 'audio24_07'
    df = pd.read_sql_query("select * from clasifications_clasifications where "
                           f"video_name=:c;",
                           conn, params={'c': f'{name}'})

    # df['new'] = pd.Series(np.random.randn(len(df['file'])), index=df.index)
    for i in range(len(df)):
        # print(df['file'][i].split('/')[-1])
        start_end = re.findall(r'[0-9]*-[0-9]*',
                               df['path'][i].split('/')[-1])
        # print((start_end[0].replace('-',''), start_end[1].replace('-','')))
        df.loc[i, 'start'] = int(start_end[0].replace('-', ''))
        df.loc[i, 'end'] = int(start_end[1].replace('-', ''))
        # df.loc[i,'new'] = re.findall(r'[0-9]*:[0-9]*:[0-9]+',
        #                             df['file'][i].split('/')[-1])[0]
        df.loc[i, 'path'] = re.findall(r'(?<=host)[/\w+/]+',
                                       df['path'][i])[0][:-11]
        # df.loc[i,'file'] = re.findall(r'(?<=host)[/\w+/]+',
        #                              df['file'][i])[0][:-3]
    df = df.sort_values(by=['start'])
    return df


def write(df, i, index_list, count, start, end, label, eol=None):
    speech_samples = samples[int(start):int(end) + 3000]
    if end - start > 24000:
        # avoid aislate false positives.
        wavfile.write("{}audio_to_txt/{}-{}-{}.wav".format(
                df['path'][i], label, start, end), sample_rate, speech_samples)
    if eol != 'EOL':
        start = df.loc[index_list[count + 1], 'start']
        end = df.loc[index_list[count + 1], 'end']
        label = df.loc[index_list[count + 1], 'label']
        return start, end, label



def write_audio_classification(df):
    begin = True
    index_list = df.index.tolist()
    index_list.append('EOL')
    count = 0
    if index_list[0] != 'EOL':
        for i in index_list[:-1]:
            if begin:
                label = df.loc[i, 'label']
                start = df.loc[i, 'start']
                end = df.loc[i, 'end']
                begin = False
            if index_list[count + 1] == 'EOL':
                write(df, i, index_list, count, start, end, label, 'EOL')
            # print(df.loc[index_list[count],'label'],
            # df.loc[index_list[count+1],'label'])
            elif df.loc[index_list[count],
                        'label'] == df.loc[index_list[count + 1], 'label']:
                if df.loc[index_list[count + 1], 'start'] - end > 32000:
                    # print(df.loc[index_list[count + 1],'start'] - end)
                    # if the politician take more tha 2 secons sice he
                    # finish to talk to start to talk again
                    # we split the prediction
                    start, end, label = write(
                            df, i, index_list, count, start, end, label)
                else:
                    end = df.loc[index_list[count + 1], 'end']
            elif df.loc[index_list[count],
                        'label'] != df.loc[index_list[count + 1], 'label']:
                start, end, label = write(
                        df, i, index_list, count, start, end, label)
            count += 1


if __name__ == '__main__':
    global conn
    conn = sqlite3.connect(os.path.join('.', "..",
                                        "tfm_server", "db.sqlite3"))
    absolute_path_input = os.path.dirname(
        os.path.abspath(__file__)) + DIR_INPUT + '/*.wav'
    files = glob.glob(absolute_path_input)
    for file in files:
        sample_rate, samples = wavfile.read(file)
        wavs = au_texto.audios(f'{FILE_PATH}/audio_to_txt/')
        df = sort_classifications()
        write_audio_classification(df)
        dataset_to_classify = pd.DataFrame()
        for wav in wavs:
            r, audio = au_texto.read_wav(wav)
            dataset_to_classify = dataset_to_classify.append(
                    au_texto.audio_text(wav, r, audio, df), ignore_index=True)
        audio_name = file.split('/')[-1]
        dataset_to_classify.to_sql(('pre_classifications_content_preclassificationscontent'
                                    ), con=conn, if_exists='append',
                                   index=False)
    conn.close()
