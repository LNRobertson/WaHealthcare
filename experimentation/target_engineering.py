# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 16:37:34 2022

@author: BetaCosine
"""
import pandas as pd
import sys
import os
os.chdir('C:/PythonDev/wa_healthcare/')
sys.path.append('./src/')

import feature_engineering_helpers as features


df_target = features.get_data('./data/healthcare_db.db', 
                              'Attorney_General_Consumer_Complaints')

df_target = df_target.loc[df_target['businesscategory'] == 'Health Care']

df_target['openeddate'] = pd.to_datetime(df_target['openeddate'], 
                                         infer_datetime_format=True)

df_target['month'] = df_target['openeddate'].dt.month
df_target['year_mo'] = df_target['openedyear'].astype(str) + '-' +\
                        df_target['month'].astype(str)

#df_target_ag = df_target[['BusinessZip', 'OpenedDate']].\
#                groupby(['BusinessZip', 'OpenedDate']).size().reset_index()

out = df_target[['businesszip','openeddate']].\
                groupby(['businesszip', pd.Grouper(freq='MS', key='openeddate')], 
                 as_index=False).size().pivot('businesszip', 'openeddate')

out = out.fillna(0)
out_mean = out.mean(axis=1)

out_mean = pd.DataFrame(out_mean).reset_index()
out_mean["businesszip"] = out_mean["businesszip"].apply(lambda x: x.strip())
out_mean = out_mean.set_index("businesszip")
out_mean.columns = ["target"]
out_mean.to_csv("./data/target_y.csv")