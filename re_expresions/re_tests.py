#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 22:16:35 2018

@author: ricardo
"""
import os
import glob
import pcre
import pandas as pd
import sqlite3

regulares_expresiones = glob.glob('database/*.csv')
otros_re = pd.DataFrame()
for regular in regulares_expresiones:
    otros_re = otros_re.append(pd.read_csv(regular), sort=True)
otros_re.rename(columns={'terms.term': 'EXPRESION REGULAR',
                         'terms.humanterm': 'TERMINO HUMANO',
                         'terms.shuffle': 'SHUFFLE'},
                inplace=True)

files = glob.glob('doc_to_class/*.csv')
# name = au_texto.audios(f'.{DIR_INPUT}')
# it work for only one file at time for now
# name = name[0].split('/')[-1]
name = 'audio24_07'
# for file in files:
global conn
conn = sqlite3.connect(os.path.join('.', "..",
                                    "tfm_server", "db.sqlite3"))
news = pd.read_sql_query("select * from pre_classifications_content_preclassificationscontent where "
                         f"video_name=:c;",
                         conn, params={'c': f'{name}'})
    # 'data_all_text_one_line.csv')
try:
    news.drop('id', inplace=True, axis=1)
except Exception:
    pass
# with open('prueba.txt', 'r') as file:
#    news = file.read()
# news = news.split('-*')

# pcre.compile('(?i)'+term['term']
d = {'comp': [], 'hum': [], 'tags': []}
for _, row in otros_re.iterrows():
    d['comp'].append(pcre.compile('(?i)'+row['EXPRESION REGULAR']))
    d['hum'].append(row['TERMINO HUMANO'])
    d['tags'].append(row['slug'])
c = 1
for i, row in news.iterrows():
    tags = {}
    human_term = []
    c += 1
    print(c)
    for j in range(len(d['comp'])):
        if isinstance(row['text'], str):
            if pcre.search(d['comp'][j], row['text']):
                if d['tags'][j] in tags:
                    tags[d['tags'][j]] += 1
                else:
                    tags[d['tags'][j]] = 1
                if not d['hum'][j] in human_term:
                    human_term.append(d['hum'][j])
    # tags = [(k, v) for k, v in tags.items()]
    tags = sorted(tags.items(), key=lambda kv: kv[1])
    if len(human_term):
        news.loc[i, 'human_term'] = str(human_term)
        news.loc[i, 'tag'] = tags[-1][0]
        news.loc[i, 'others_tags'] = ', '.join(
                [tag for tag, counter in tags])
conn.close()
# news.dropna(inplace=True)
# file = file.split('/')[1].replace('.*', '')
#news.to_csv(f'doc_class/{file}resultados.csv', index=False)
