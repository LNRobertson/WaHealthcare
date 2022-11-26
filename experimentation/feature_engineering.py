# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 23:00:09 2022

@author: BetaCosine
"""
import pandas as pd

from joblib import dump, load
import sys
import os
os.chdir('C:/PythonDev/wa_healthcare/')
sys.path.append('./src/')

import feature_engineering_helpers as features

grouper = ['primarypracticezip']

numeric_cols = ['annualweeksworked',
                'birthyear',
                'highesteducationyear',
                'initialcredentialyear',
                'numberyearspracticewashington',
                'numberyearsprimarypracticelocation',
                'paidhourspatientcareinstate']

dummy_cols = ['activecredentialotherstate',
              'communicateotherlanguage',
              'highesteducationonline',
              'sex',
              'workstatus']

variation_cols = ['credentialtype',
                  'primarypracticesetting',
                  'race']

df = features.get_data('./data/healthcare_db.db',
                       'Washington_Health_Workforce_Survey_Data')

numeric_features = df[grouper+numeric_cols].groupby(grouper).mean()

dummy_features = [features.dummy_features_bygroup(df, grouper, d)
                  for d in dummy_cols]

variation_features = [features.variation_features_bygroup(df, grouper[0], v)
                      for v in variation_cols]

dummy_features = pd.concat(dummy_features, axis=1)
variation_features = pd.concat(variation_features, axis=1)

df_features = pd.concat([numeric_features, dummy_features, variation_features],
                        axis=1)         

#fill missing values with mean imputation
df_features = df_features.apply(lambda x: x.fillna(x.mean()),axis=0)

df_features = df_features.reset_index()
df_features["primarypracticezip"] = df_features["primarypracticezip"].\
                                    apply(lambda x: x.strip())

df_features = df_features.set_index("primarypracticezip")

#merge with target variable
out_mean = pd.read_csv("./data/target_y.csv")
out_mean = out_mean.set_index("businesszip")
df_combined = df_features.merge(out_mean, how="inner", left_index = True, 
                                right_index=True)
cols = list(df_combined.columns)
cols = ["zip"]+cols
df_combined = df_combined.reset_index()
df_combined.columns = cols
df_combined.to_csv("./data/feature_target_set.csv", index=False)
