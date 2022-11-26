# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 10:46:37 2022

@author: BetaCosine
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

import matplotlib.pyplot as plt
from joblib import dump, load


import sys
import os
os.chdir('C:/PythonDev/wa_healthcare/')
sys.path.append('./src/')

df = pd.read_csv("./data/feature_target_set.csv")

#train test splits

y = df[["target"]]

X = df.iloc[:,1:23]

features = list(X.columns)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, 
                                                    random_state=42)

#minmax normalization
scaler = MinMaxScaler()
scaler.fit(X_train)

#save scaler "model"
dump(scaler, "./models/minmax_scaler.joblib")

X_train, X_test = scaler.fit_transform(X_train), scaler.fit_transform(X_test)

#model training with feature selection

reg_selector = SelectFromModel(estimator=LinearRegression())
reg_selector.fit(X_train, y_train)
reg_model = LinearRegression()
reg_model.fit(reg_selector.transform(X_train), y_train)
y_train_reg = reg_model.predict(reg_selector.transform(X_train))
y_test_reg = reg_model.predict(reg_selector.transform(X_test))

svm_selector = SelectFromModel(estimator=SVR(kernel='linear'))
svm_selector.fit(X_train,y_train)
svm_model = SVR()
svm_model.fit(svm_selector.transform(X_train), y_train)
y_train_svm = svm_model.predict(svm_selector.transform(X_train))
y_test_svm = svm_model.predict(svm_selector.transform(X_test))

rf_selector = SelectFromModel(estimator=RandomForestRegressor())
rf_selector.fit(X_train,y_train)
rf_model = RandomForestRegressor()
rf_model.fit(rf_selector.transform(X_train), y_train)
y_train_rf = rf_model.predict(rf_selector.transform(X_train))
y_test_rf = rf_model.predict(rf_selector.transform(X_test))

#evaluate features selected

reg_features = reg_selector.get_support().reshape(22,1)
svm_features = svm_selector.get_support().reshape(22,1)
rf_features = rf_selector.get_support().reshape(22,1)

reg_coefs = reg_selector.estimator_.coef_.reshape(22,1)
svm_coefs = svm_selector.estimator_.coef_.reshape(22,1)
rf_coefs = rf_selector.estimator_.feature_importances_.reshape(22,1)

all_features = np.concatenate([np.asarray(features).reshape(22,1), reg_features, 
                               reg_coefs, svm_features, svm_coefs,
                               rf_features, rf_coefs],axis=1)

#evaluate model performance using RMSE

reg_train_mse = mean_squared_error(y_train, y_train_reg, squared=False)
reg_test_mse = mean_squared_error(y_test, y_test_reg, squared=False)
reg_diff = reg_test_mse - reg_train_mse

svm_train_mse = mean_squared_error(y_train, y_train_svm, squared=False)
svm_test_mse = mean_squared_error(y_test, y_test_svm, squared=False)
svm_diff = svm_test_mse - svm_train_mse

rf_train_mse = mean_squared_error(y_train, y_train_svm, squared=False)
rf_test_mse = mean_squared_error(y_test, y_test_reg, squared=False)
rf_diff = rf_test_mse - rf_train_mse

#plot performance metrics

plt.bar(['reg','svm','rf'],[reg_test_mse, svm_test_mse, rf_test_mse])
plt.ylim([.2712,.2719])
plt.title('title name')
plt.xlabel('RMSE by Model')
plt.ylabel('Value')
plt.show()

plt.bar(['reg','svm','rf'],[reg_diff, svm_diff, rf_diff])
plt.ylim([.1,.15])
plt.title('title name')
plt.xlabel('RMSE by Model')
plt.ylabel('Value')
plt.show()

#save winning model

dump(reg_selector, "./models/regression_feature_selector_1.0.joblib")
dump(reg_model, "./models/regression_model_1.0.joblib")

