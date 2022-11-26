# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 10:46:37 2022

@author: BetaCosine
"""
import pandas as pd
import numpy as np

from joblib import load


def main(df_features):
    
    #save scaler "model"
    scaler = load("./models/minmax_scaler.joblib")
    feature_selector = load("./models/regression_feature_selector_1.0.joblib")
    model = load("./models/regression_model_1.0.joblib")
    
    df_features = scaler.transform(df_features)
    df_features = feature_selector.transform(df_features)
    scores = model.predict(df_features)
    return scores
