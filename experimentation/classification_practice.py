# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 13:51:43 2022

@author: BetaCosine
"""

import pandas as pd
from joblib import load
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_curve, roc_auc_score
import matplotlib.pyplot as plt

import os
os.chdir("C:/PythonDev/wa_healthcare")

df = pd.read_csv("./data/feature_target_set.csv")

#create binary target variable

df["Target"] = (df["Target"] >= df["Target"].median()) * 1

#train test split with normalization

y = df[["Target"]]

X = df.iloc[:,1:23]

features = list(X.columns)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, 
                                                    random_state=42)

scaler = load("./models/minmax_scaler.joblib")

X_train, X_test = scaler.fit_transform(X_train), scaler.fit_transform(X_test)


#train a classification model

rf = RandomForestClassifier(max_depth=2, random_state=0)

rf.fit(X_train, y_train)

y_test_hat = rf.predict(X_test)

report = classification_report(y_test, y_test_hat, output_dict=True)
report_df = pd.DataFrame(report).transpose()

#roc curve

y_pred_proba = rf.predict_proba(X_test)[::,1]
fpr, tpr, threshold = roc_curve(y_test, y_pred_proba)
auc = roc_auc_score(y_test, y_pred_proba)

plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
plt.legend(loc=4)
plt.show()
    