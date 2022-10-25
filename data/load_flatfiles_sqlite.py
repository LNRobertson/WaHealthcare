# -*- coding: utf-8 -*-


import pandas as pd
import sqlite3
import datetime
import os
os.chdir("C:/PythonDev/")



#get list of flat files for data load to db
def return_data(path, file_type='.csv'):
    data_list = []
    for file in os.listdir(path):
        if file.lower().endswith(file_type):
            data_list.append(file)
    return data_list
    
flat_files  = return_data("./wa_healthcare/data/")

#connect to database
database_name = "healthcare_db.db"

con = sqlite3.connect("./wa_healthcare/data/"+database_name)

#enter data into database
for file in flat_files:
    if file.startswith("Attorney") or file.startswith("Washington"):
        df = pd.read_csv("./wa_healthcare/data/"+file)
        df['sys_src_ld_dt'] = datetime.datetime.now()
        table_name = file.split(".csv")[0]
        df.columns = map(str.lower, df.columns)
        if table_name == 'Attorney_General_Consumer_Complaints':
            df['month'] = pd.DatetimeIndex(df['openeddate']).month
            df['yearmo'] = df['openedyear'] + df['month']
        df.to_sql(table_name,con, if_exists='append', index=False)

#playing with SQL

sql = """
SELECT ABMSCertified 
FROM Washington_Health_Workforce_Survey_Data 
WHERE ABMSCertified NOT NULL
"""

test = pd.read_sql(sql, con)

sql = """
CREATE TEMP VIEW healthcare_survey_r
AS
SELECT
	primarypracticezip, annualweeksworked, birthyear, initialcredentialyear,
	paidhourspatientcareinstate,
	CASE
	WHEN highesteducationyear < 1950 THEN NULL
	ELSE highesteducationyear
	END AS ed_year_recoded,
	CASE
	WHEN numberyearspracticewashington = -1 THEN 0
	ELSE numberyearspracticewashington
	END AS prim_years_recoded,
	CASE 
	WHEN numberyearsprimarypracticelocation = -1 THEN 0
	WHEN numberyearsprimarypracticelocation > 75 THEN NULL
	END AS prim_loc_years_recoded
FROM
washington_health_workforce_survey_data
"""

con.execute(sql)

test = pd.read_sql("SELECT * FROM healthcare_survey_r", con)
