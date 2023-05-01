import streamlit as st
import streamlit_pandas as sp
import pandas as pd
import re
import random

df = pd.read_csv("userfsktm19202-2.csv")

# Rename the 'time' column to 'access_date'
df.rename(columns={'time': 'access_date'}, inplace=True)

# Convert the 'access_date' column to a date-only format
df['access_date'] = pd.to_datetime(df['access_date']).dt.date

# Create two DataFrames based on the condition
df_with_course = df[df['Event_context'].str.contains('Course')]
df_without_course = df[~df['Event_context'].str.contains('Course')]

# Print the first few rows of each DataFrame to verify the split
print('DataFrame with Course:')
print(df_with_course.head())
print('\nDataFrame without Course:')
print(df_without_course.head())

# df_salihan = pd.read_csv('Salihan.csv')
# print(df_salihan['KOD KURSUS'].unique())
# print("df_without_course length: ", len(df_without_course))

# course_codes = {'69141': 'SIM3251', '69142': 'SSE4306', '69143': 'SKR3307', ... } # add all course module IDs and their corresponding course codes
#
# def get_course_code(description):
#     match = re.search(r"course module id '(\d+)'", description)
#     if match:
#         course_module_id = match.group(1)
#         if course_module_id in course_codes:
#             return course_codes[course_module_id]
#     return None
#
# df_without_course['KOD KURSUS'] = df_without_course['Description'].apply(get_course_code)

# define list of course codes
course_codes = ['SIM3251', 'SSE4306', 'SKR3307', 'SSK4506', 'SKR3305', 'SSK4610', 'SIM4207',
                'SKM4212', 'SIM4208', 'SSE4351', 'SKR4307', 'SSK4602', 'SSE3150', 'SKR4202',
                'SSK3101', 'SSK3408', 'SSK3313', 'SSK3118', 'SKR3504', 'SSK3207', 'SSK3003',
                'SSK3100', 'SKR3306', 'SKR3202', 'SSK4617', 'SSE4356', 'SKM4201', 'SKR3308',
                'SSK4407', 'SSK4505', 'SSE3305', 'SKR3201', 'SSK4507', 'SSK4508', 'SSK3102',
                'SSE3151', 'SKM3203', 'SSE4301', 'SKM4310', 'SKR4301']

# add new column with random course codes
df_without_course['KOD KURSUS'] = [random.choice(course_codes) for _ in range(len(df_without_course))]
df['KOD KURSUS'] = [random.choice(course_codes) for _ in range(len(df))]
df_with_course['KOD KURSUS'] = [random.choice(course_codes) for _ in range(len(df_with_course))]
# print(df.head())

# Save to a CSV files
df.to_csv('userfsktm_kodkursus.csv', index=False)
df_with_course.to_csv('df_with_course.csv', index=False)
df_without_course.to_csv('df_without_course.csv', index=False)