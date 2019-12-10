%reset -f
import pandas as pd
import numpy as np

df= pd.read_csv('grades.csv')

df.info()
df.head()

# Remove Username and Student ID columns.
df.drop(['Username', 'Student ID'], axis=1, inplace=True)

df.head()

# Remove everything after the '[' character in the column names. For example, the Chapter 1 quiz column downloaded from Blackboard is:
# 'Chapter 1 [Total Pts: 11.11 Score] |1631060'
df.columns= df.columns.str.split('[').str[0]

# Remove white spaces from column names
df.columns= df.columns.str.rstrip()
df.drop(['Weighted Total', 'Total'], axis=1, inplace=True)
df.info()
df.head()

# Reorder columns
df= df[['Last Name', 'First Name', 'Module B', 'Chapter 1', 'Chapter 2', 'Chapter 3', 'Chapter 4', 'Chapter 5', 'Chapter 6', 'Chapter 7', 'Chapter 11', 'Chapter 12', 'Midterm', 'Final']]

df.head()

# Replace missing values with 0. Missing values indicate a student did not take a particular assignment.
df= df.fillna(0)

# Identify the minimum quiz score. Note this excludes the Midterm and Final columns. I "drop" the students' lowest quiz score before calculating final grades.
df['quiz_min']=df[['Module B', 'Chapter 1', 'Chapter 2', 'Chapter 3', 'Chapter 4', 'Chapter 5', 'Chapter 6', 'Chapter 7', 'Chapter 11', 'Chapter 12']].min(axis=1)

df.head()

# Mathematically, dropping the lowest quiz score is done by adding up all of the quizzes and subtracting the minimum score from the total. Note that ties for lowest score do not matter.
# Calculates total quiz score by summing up over the quizzes, subtracting the minimum, and adding .01. The .01 is added because my class has 10 quizzes, I drop one, and each quiz is worth 11.11.
df['quiz_tot']= df[['Module B', 'Chapter 1', 'Chapter 2', 'Chapter 3', 'Chapter 4', 'Chapter 5', 'Chapter 6', 'Chapter 7', 'Chapter 11', 'Chapter 12']].sum(axis=1) - df['quiz_min'] + .01

df.head()

# I have a policy that if a student misses the midterm for any reason, then the final is double counted.
# Any missing Midterm values have now been set to 0. Below conditions on Midterms =0 and sets Midterm equal to the Final.
df.loc[df['Midterm']==0, 'Midterm']= df['Final']

############# !!!!!!!!!!!!!!!!!!!!!!!!  A curve is hard coded below !!!!!!!!!!!!!!! #########################
# Curve is added at the end here with the + 10 in total points.
df['total_points']= df['quiz_tot'] + df['Final'] + df['Midterm'] + 10
df['grade']= df['total_points']/300

# Eyeball the sorted final grades.
df[['Last Name', 'First Name', 'grade']].sort_values(by=['grade'], ascending=False)
