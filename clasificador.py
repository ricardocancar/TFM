#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 13:12:58 2018

@author: ricardo
"""

import pandas as pd
import json
path = '/home/ricardo/Documents/TFM/clasification_news/data_train/vivienda.json'
with open(path) as datafile:
    data = json.load(datafile)
    data = eval(data)
df = pd.DataFrame(data)
df = df['terms']
