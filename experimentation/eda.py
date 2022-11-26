# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 19:21:18 2022

@author: BetaCosine
"""
import pandas as pd
import sqlite3
import os
os.chdir("C:/PythonDev/wa_healthcare/")

#check nulls and remove columns

df = pd.read_csv("./data/Washington_Health_Workforce_Survey_Data.csv")

nulls = df.isnull().sum().to_frame()
nulls['proportion'] = nulls/df.count().max()
keep = nulls.loc[nulls['proportion'] < .3]
keep = keep.reset_index()
keep_cols = list(keep['index'].values)

dfr = df[keep_cols] 

#numeric data
describe = dfr.describe()    
numeric_cols = list(describe.columns)

dfr[numeric_cols[-1]].hist()
d = dfr.loc[dfr[numeric_cols[-1]] > 50]
dfr[numeric_cols[-1]].hist()

corr_matrix = dfr[numeric_cols].corr()

#example transform based on EDA

def year_recode(number):
    if number > 1950:
        return number
    else:
        return None
    
dfr['Highest_Ed_Year_1950'] = dfr['HighestEducationYear'].apply(year_recode)

describe_recode = dfr['Highest_Ed_Year_1950'].describe()

#nonnumeric data

non_num_cols = [k for k in keep_cols if k not in numeric_cols]

unique_vals = [(k, dfr[k].nunique()) for k in non_num_cols]

freq_dist = dfr[non_num_cols[10]].value_counts()/dfr.count().max()
freq_dist.plot.bar()
freq_dist.hist()

a = df[['PrimaryPracticeZip','CredentialType']]\
    .groupby('PrimaryPracticeZip')['CredentialType'].nunique()

z = df[['PrimaryPracticeZip']]\
    .groupby('PrimaryPracticeZip').size()

d = df[['PrimaryPracticeZip','CredentialType']]\
    .groupby('PrimaryPracticeZip')['CredentialType'].nunique() / df[['PrimaryPracticeZip']]\
        .groupby('PrimaryPracticeZip').size()

def variation_features_bygroup(df, grouper, non_num_col):
    
    variation = df[[grouper,non_num_col]]\
        .groupby(grouper)[non_num_col].nunique()

    total_entries = df[[grouper]].groupby(grouper).size()
    
    variation_by_total_entries = df[[grouper,non_num_col]]\
        .groupby(grouper)[non_num_col].nunique() / df[[grouper]]\
        .groupby(grouper).size()
    
    combined = pd.concat([variation, total_entries, variation_by_total_entries],
                         axis=1)
    
    combined.columns = [non_num_col+'_variation', non_num_col+'_total_entries',
                        non_num_col+'_var_by_total']
    
    return combined


    
