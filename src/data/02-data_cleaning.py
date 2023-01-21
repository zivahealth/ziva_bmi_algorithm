# Import packages
import pandas as pd
import numpy as np
import os
from pathlib import Path


# Define functions
def import_demographics(year_dir_path):
    # Find filepath
    for subdir, dirs, files in os.walk(year_dir_path + "Demographics/"):
        for file in files:
            if file.endswith(".csv") & ("DEMO" in file):
                filepath = os.path.join(subdir, file)

    demographics = pd.read_csv(filepath)
    dems = demographics[['SEQN', 'RIAGENDR', 'RIDAGEMN', 'RIDAGEYR', 'RIDEXPRG', 'RIDRETH1']].copy()
    dems.set_axis(
        [
            'id',
            'sex',                  # 1: Male, 2: Female
            'age_months',
            'age_yrs',
            'pregnancy_status',     # 1: Pregnant, 2: Not pregnant, 3: Unknown
            'race'                  
        ], 
        axis=1, 
        inplace=True
    )
    dems = dems.astype({
        "id": "int",
        "sex": "int",
        "race": "int"
    })
    dems.set_index('id', inplace=True)

    return dems

def import_body_data(body_data_dir_path):
    # Find filepath for body data
    for subdir, dirs, files in os.walk(body_data_dir_path + "Examination/"):
        for file in files:
            if file.endswith(".csv") & ("BMX" in file):
                filepath_measurements = os.path.join(subdir, file)
                
    # Import body measurements
    body_measurements = pd.read_csv(filepath_measurements)
    measurements = body_measurements[['SEQN', 'BMXWT', 'BMXHT', 'BMXWAIST']].copy()
    measurements.set_axis(['id', 'weight_kg', 'height_cm', 'waist_circum_cm'], axis=1, inplace=True)
    measurements = measurements.astype({"id": "int"})
    measurements.set_index('id', inplace=True)

    # Drop rows with missing height or weight
    measurements = measurements[measurements['weight_kg'].notna() & measurements['height_cm'].notna()]

    # Find filepath for body data
    for subdir, dirs, files in os.walk(body_data_dir_path + "Questionnaire/"):
        for file in files:
            if file.endswith(".csv") & (("SMQ_" in file) | ("SMQ." in file)):
                filepath_smoker = os.path.join(subdir, file)

    # Import smoker indication
    smoker_indication = pd.read_csv(filepath_smoker)
    smoker = smoker_indication[[
        'SEQN', 
        'SMQ020', # Smoked at least 100 cigarettes in life (1: Yes, 2: No, 7: Refused, 9: Don't know)
        'SMQ040'  # Do you know smoke cigarettes (1: Every day, 2: Some days, 3: Not at all, 7: Refused, 9: Don't know)
    ]].copy()
    smoker.set_axis([
        'id', 
        'has_smoked', 
        'is_smoker'
    ], axis=1, inplace=True)
    smoker = smoker.astype({"id": "int"})
    smoker.set_index('id', inplace=True)

    # Join smoker and body measurements data
    measurements_smoker = pd.merge(measurements, smoker, how='left', on='id')

    return measurements_smoker

def import_fat_pct(fat_pct_dir_path):
    # Find filepath for percent body fat data
    for subdir, dirs, files in os.walk(fat_pct_dir_path + "Examination/"):
        for file in files:
            if file.endswith(".csv") & ("dxx" in file):
                filepath = os.path.join(subdir, file)

    # Import percent body fat data
    fat_percentage = pd.read_csv(filepath)
    fat_pct = fat_percentage[['SEQN', '_MULT_', 'DXDTOPF']]
    fat_pct.set_axis(['id', 'M', 'total_fat_pct'], axis=1, inplace=True)
    fat_pct = fat_pct.astype({"id": "int", "M": "int"})

    # Drop rows with missing data
    # fat_pct = fat_pct[fat_pct['total_fat_pct'].notna()]

    return fat_pct

def import_year_predictors(year_range):
    # Import predictors
    demographics = import_demographics("./../../data/raw/NHANES_" + year_range + "/")
    measurements = import_body_data("./../../data/raw/NHANES_" + year_range + "/")

    # Join demographic and measurement data
    predictors = pd.merge(measurements, demographics, how='left', on='id')

    return predictors

def import_predictors():
    # Import datasets from each year
    predictors99 = import_year_predictors("1999-2000")
    predictors99['years'] = "1999-2000"
    predictors01 = import_year_predictors("2001-2002")
    predictors01['years'] = "2001-2002"
    predictors03 = import_year_predictors("2003-2004")
    predictors03['years'] = "2003-2004"
    predictors05 = import_year_predictors("2005-2006")
    predictors05['years'] = "2005-2006"

    # Concatenate all datasets into one
    predictors = pd.concat([predictors99, predictors01, predictors03, predictors05], axis=0)

    # CLEANING
    predictors['sex'] = predictors['sex'] - 1

    return predictors

def import_response():
    # Import fat_pct from each year
    response99 = import_fat_pct("./../../data/raw/NHANES_1999-2000/")
    response01 = import_fat_pct("./../../data/raw/NHANES_2001-2002/")
    response03 = import_fat_pct("./../../data/raw/NHANES_2003-2004/")
    response05 = import_fat_pct("./../../data/raw/NHANES_2005-2006/")

    # Concatenate all datasets into one
    response = pd.concat([response99, response01, response03, response05], axis=0)

    return response








## Join imputed values onto predictors

Path('./../../data/interim/01-filtered_columns/').mkdir(parents=True, exist_ok=True)

# Generate predictors and responses
predictors = import_predictors()
predictors.to_csv("./../../data/interim/01-filtered_columns/predictors.csv")
response = import_response()
response.to_csv("./../../data/interim/01-filtered_columns/response.csv")

# M = 1
responseM1 = response.copy()[response['M'] == 1]
responseM1.set_index('id', inplace=True)
dataM1 = pd.merge(predictors.copy(), responseM1, how="inner", on="id")
dataM1.to_csv("./../../data/interim/01-filtered_columns/M1_data.csv")

# M = 2
responseM2 = response.copy()[response['M'] == 2]
responseM2.set_index('id', inplace=True)
dataM2 = pd.merge(predictors.copy(), responseM2, how="inner", on="id")
dataM2.to_csv("./../../data/interim/01-filtered_columns/M2_data.csv")

# M = 3
responseM3 = response.copy()[response['M'] == 3]
responseM3.set_index('id', inplace=True)
dataM3 = pd.merge(predictors.copy(), responseM3, how="inner", on="id")
dataM3.to_csv("./../../data/interim/01-filtered_columns/M3_data.csv")

# M = 4
responseM4 = response.copy()[response['M'] == 4]
responseM4.set_index('id', inplace=True)
dataM4 = pd.merge(predictors.copy(), responseM4, how="inner", on="id")
dataM4.to_csv("./../../data/interim/01-filtered_columns/M4_data.csv")

# M = 5
responseM5 = response.copy()[response['M'] == 5]
responseM5.set_index('id', inplace=True)
dataM5 = pd.merge(predictors.copy(), responseM5, how="inner", on="id")
dataM5.to_csv("./../../data/interim/01-filtered_columns/M5_data.csv")






## Run transformation on smoking columns

# Create folder to store datasets
Path('./../../data/interim/02-smokers_cleaned/').mkdir(parents=True, exist_ok=True)


# THIS CODE IS TAKEN FROM "eda.ipynb"

predictors_smoking = predictors.copy()

# Drop 'age_months' since there is no missing data in age_yrs
predictors_smoking.drop(['age_months'], axis=1, inplace=True)

# Construct 'smoker_status' column
predictors_smoking['smoker_status'] = np.nan

# Set 'smoker_status' column to 0 for non-smokers (who have never been smokers)
predictors_smoking.loc[predictors_smoking['has_smoked'] == 2, 'smoker_status'] = 0

# Set 'smoker_status' column to 1 for active smokers
predictors_smoking.loc[(predictors_smoking['is_smoker'] == 1) | (predictors_smoking['is_smoker'] == 2), 'smoker_status'] = 1

# Set 'smoker_status' column to 2 for former smokers
predictors_smoking.loc[predictors_smoking['is_smoker'] == 3, 'smoker_status'] = 2

# Drop 'has_smoked' and 'is_smoker' columns now that they are consolidated into 'smoker_status'
predictors_smoking.drop(['has_smoked', 'is_smoker'], axis=1, inplace=True)

# Reorder columns
cols_reordered = [
    'weight_kg', 
    'height_cm', 
    'sex', 
    'age_yrs', 
    'race', 
    'waist_circum_cm', 
    'smoker_status', 
    'pregnancy_status', 
    'years'
]

# Update predictors dataset and rerun code joining each imputation on the response
predictors = predictors_smoking[cols_reordered]

predictors.to_csv("./../../data/interim/02-smokers_cleaned/predictors.csv")

response.to_csv("./../../data/interim/02-smokers_cleaned/response.csv")

# M = 1
responseM1 = response.copy()[response['M'] == 1]
responseM1.set_index('id', inplace=True)
dataM1 = pd.merge(predictors.copy(), responseM1, how="inner", on="id")
dataM1.to_csv("./../../data/interim/02-smokers_cleaned/M1_data.csv")

# M = 2
responseM2 = response.copy()[response['M'] == 2]
responseM2.set_index('id', inplace=True)
dataM2 = pd.merge(predictors.copy(), responseM2, how="inner", on="id")
dataM2.to_csv("./../../data/interim/02-smokers_cleaned/M2_data.csv")

# M = 3
responseM3 = response.copy()[response['M'] == 3]
responseM3.set_index('id', inplace=True)
dataM3 = pd.merge(predictors.copy(), responseM3, how="inner", on="id")
dataM3.to_csv("./../../data/interim/02-smokers_cleaned/M3_data.csv")

# M = 4
responseM4 = response.copy()[response['M'] == 4]
responseM4.set_index('id', inplace=True)
dataM4 = pd.merge(predictors.copy(), responseM4, how="inner", on="id")
dataM4.to_csv("./../../data/interim/02-smokers_cleaned/M4_data.csv")

# M = 5
responseM5 = response.copy()[response['M'] == 5]
responseM5.set_index('id', inplace=True)
dataM5 = pd.merge(predictors.copy(), responseM5, how="inner", on="id")
dataM5.to_csv("./../../data/interim/02-smokers_cleaned/M5_data.csv")





## Final cleaning: Update to account for missing data

# Remove rows with missing fat pct (our response variable) from each imputed dataset
dataM1_clean = dataM1.copy()[dataM1['total_fat_pct'].notna()]
dataM2_clean = dataM2.copy()[dataM2['total_fat_pct'].notna()]
dataM3_clean = dataM3.copy()[dataM3['total_fat_pct'].notna()]
dataM4_clean = dataM4.copy()[dataM4['total_fat_pct'].notna()]
dataM5_clean = dataM5.copy()[dataM5['total_fat_pct'].notna()]

# Drop the pregnancy status column since none of the pregnant subjects had fat pct measurements
predictors_clean = predictors.drop(['pregnancy_status'], axis=1)

# Drop rows with missing waist circumference since know we want to implement this variable
predictors_clean = predictors_clean[predictors_clean['waist_circum_cm'].notna()]

# Save predictors file
predictors_clean.to_csv("./../../data/processed/predictors.csv")

# Repeat changes to predictors and save clean imputation datasets
data_clean = [dataM1_clean, dataM2_clean, dataM3_clean, dataM4_clean, dataM5_clean]

for M_num, dataset in enumerate(data_clean):
    dataset_updated = dataset.drop(['pregnancy_status'], axis=1)
    dataset_updated = dataset_updated[dataset_updated['waist_circum_cm'].notna()]
    dataset_updated.to_csv('./../../data/processed/M' + str(M_num+1) + '_data.csv')