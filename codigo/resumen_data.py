#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 22:23:06 2019

@author: ricardo
"""
import os
import pcre
import pandas as pd
import sqlite3
import logging

logging.basicConfig(filename="./log/resume_data.log", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

global conn
conn = sqlite3.connect(os.path.join('.', "..",
                                    "tfm_server", "db.sqlite3"))
news = pd.read_sql_query("select * from content_classificated_clasificationscontent", con=conn)
    # 'data_all_text_one_line.csv')
try:
    news.drop('id', inplace=True, axis=1)
except Exception as e:
    logger.warning(f'{e}')

total_clasifications = news.groupby('tag').count()
clasifications_by_politictis = news.groupby(['label','tag']).count()


total_clasifications.rename(index={'': 'unknown'}, columns={
        'video_name': 'numbers'}, inplace=True)
total = total_clasifications['numbers'].sum()
total_clasifications['numbers'] = (total_clasifications['numbers']/total)*100
total_clasifications.reset_index(level=0, inplace=True)
total_clasifications.rename(columns={
        'tag': 'content'}, inplace=True)
total_clasifications = total_clasifications[['content', 'numbers']]

clasifications_by_politictis.reset_index(level=0, inplace=True)
clasifications_by_politictis.reset_index(level=0, inplace=True)
clasifications_by_politictis['tag'][clasifications_by_politictis['tag']== ''] = 'unknown'
clasifications_by_politictis.rename(columns={
        'tag': 'content',
        'label': 'political',
        'video_name': 'numbers'}, inplace=True)
clasifications_by_politictis = clasifications_by_politictis[
        ['political', 'content', 'numbers']]
#total_clasifications.to_sql(('resumen_values_resumen'),
#            con=conn, if_exists='append', index=False)
#clasifications_by_politictis.to_sql(('political_clasification_politicalclasification'),
#            con=conn, if_exists='append', index=False)
print('done')
