#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 21:34:12 2019

@author: ricardo
"""
import csv
import sqlite3
import argparse
import looging
# import au_texto

logging.basicConfig(filename="./log/csv_to_sqlite.log", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',
                        help='name of the video',
                        required=True)

    ret = parser.parse_args()
    return ret


conn = sqlite3.connect("./../tfm_server/db.sqlite3")
cursor = conn.cursor()
# args = get_args()

with open('predictions.csv') as csv_file:
    try:
        # it work for only one file at time for now
        args = get_args()
        name = args.input
        name = name.split('/')[-1]
        print(f'name: {name}')
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                cursor.execute('''INSERT INTO clasifications_clasifications(video_name, path, label, score)
                               VALUES(?,?,?,?)''', (name, row[2],
                               row[1], float(row[0])))
            line_count += 1
            conn.commit()
    except Exception as e:
        logger.warning(f'{e}')
conn.close()
