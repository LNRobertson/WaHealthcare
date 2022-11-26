# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 22:36:00 2022

@author: BetaCosine
"""
import pandas as pd
import sqlite3


def get_data(database_path, table_name):
    con = sqlite3.connect(database_path)
    df = pd.read_sql("SElECT * FROM %s" % table_name, con)
    return df
    
    
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


def dummy_features_bygroup(df, grouper, non_num_col):
    
    dumdums = pd.get_dummies(df[non_num_col], drop_first=True)
    dumdums = pd.concat([df[grouper], dumdums], axis=1)
    
    aggregate = dumdums.groupby(grouper).sum()
    cols = list(aggregate.columns)
    cols = [non_num_col + "_" + str(x) for x in cols]
    aggregate.columns = cols
    
    return aggregate
    