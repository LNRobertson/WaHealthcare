# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 14:34:43 2022

@author: BetaCosine
"""
import pandas as pd
import sqlite3
from sodapy import Socrata
import re
import logging
#import os
#os.chdir("C:/PythonDev/wa_healthcare")


def get_most_recent_sqlite_dt(table, col, con):
    sql = '''
    SELECT MAX(%s) AS %s FROM %s
    ''' % (col, col, table)
    date = pd.read_sql(sql, con)
    date = date[col].iloc[0].split(' ')[0]
    if re.search("/", date):
        re_date = date.split("/")
        reformatted_date = re_date[2]+"-"+re_date[0]+"-"+re_date[1]
        return reformatted_date
    else:
        return date

def return_all_data(socrata_dataset_id, date, date_col):
    client = Socrata("data.wa.gov", None)
    dfs = []

    for i in range(1000):
        
        data = client.get(socrata_dataset_id, 
                          where="%s > '%s'" % (date_col, date), 
                          limit = 1000, offset = 1000 * i)
        if len(data) == 0:
            break
        else:
            data_df = pd.DataFrame.from_records(data)
            dfs.append(data_df)
    if dfs:
        df = pd.concat(dfs)
        return df
    else:
        logger.info("NO NEW DATA FROM API")

def main():    

    database_name = "healthcare_db.db"
    con = sqlite3.connect("./data/"+database_name)
    
    survey_table = "Washington_Health_Workforce_Survey_Data"
    complaint_table = "Attorney_General_Consumer_Complaints"
    survey_max_date = get_most_recent_sqlite_dt(survey_table,
                                                'DateCreated', con)
    complaint_max_date = get_most_recent_sqlite_dt(complaint_table,
                                                   'OpenedDate', con)
    healthcare_survey_id = "cvrw-ujje"
    consumer_complaints_id = "gpri-47xz"
    
    df_survey = return_all_data(healthcare_survey_id, survey_max_date,
                                'datecreated')
    df_complaint = return_all_data(consumer_complaints_id, complaint_max_date, 
                                   'openeddate')
    
    complaint_cols = con.execute("PRAGMA table_info(%s)" % complaint_table).\
                                fetchall()
    
    df_survey.to_sql(survey_table,con, if_exists='append', index=False)
    df_complaint.to_sql(survey_table,con, if_exists='append', index=False)
    logger.info("DataBase Tables Have Been Updated")

logging.basicConfig(filename='./db_update.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)    