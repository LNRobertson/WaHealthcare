# -*- coding: utf-8 -*-

import sqlite3
import os
os.chdir("C:/PythonDev/wa_healthcare")


database = "healthcare_db.db"

con = sqlite3.connect("./data/"+database)

sql = """
CREATE VIEW healthcare_survey_r
AS
SELECT
	PrimaryPracticeZip, AnnualWeeksWorked, BirthYear, InitialCredentialyear,
	PaidhoursPatientCareInState, ActiveCredentialOtherState, HighestEducationOnline,
	Sex, WorkStatus, CredentialType, PrimaryPracticeSetting, Race,
	CASE
	WHEN HighestEducationYear < 1950 THEN NULL
	ELSE HighestEducationYear 
	END AS ed_year_recoded,
	CASE
	WHEN NumberYearsPracticeWashington = -1 THEN 0
	ELSE NumberYearsPracticeWashington 
	END AS prim_years_recoded,
	CASE 
	WHEN NumberYearsPrimaryPracticeLocation = -1 THEN 0
	WHEN NumberYearsPrimaryPracticeLocation > 75 THEN NULL
	END AS prim_loc_years_recoded
FROM
Washington_Healthcare_Workforce_Survey_Data
"""

con.execute(sql)
