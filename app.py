# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 23:29:26 2022

@author: BetaCosine
"""
import os
import sys
import pandas as pd

os.chdir("C:/PythonDev/wa_healthcare/")
sys.path.append("./src/")

import database_update_api as dua
import feature_engineering_api as fea
import model_scoring_api as msa

dua.main()
df_features = fea.main()
scores = msa.main(df_features)
scores = pd.DataFrame(scores)
scores.to_csv("./results.csv")
