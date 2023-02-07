# A script for generating simulated data to reflect the desired behavior of the scoring algorithm

# Install packages
import numpy as np
import pandas as pd

# Define body fat percentage ranges
bfp_ranges_f_twenties = [0, 9.5, 14, 16.4, 19.5, 22.8, 27.2, 58.6, 1]
bfp_ranges_f_thirties = [0, 9.5, 14, 17.5, 20.9, 24.7, 29.2, 58.6, 1]
bfp_ranges_f_forties = [0, 9.5, 14, 19.9, 23.9, 27.7, 32, 58.6, 1]
bfp_ranges_f_fifties = [0, 9.5, 14, 22.6, 27.1, 30.5, 34.6, 58.6, 1]
bfp_ranges_f_sixties = [0, 9.5, 14, 23.3, 28, 31.4, 35.5, 58.6, 1]

# Save female ranges
bfp_ranges_f = [bfp_ranges_f_twenties, bfp_ranges_f_thirties, bfp_ranges_f_forties, bfp_ranges_f_fifties, bfp_ranges_f_sixties]

bfp_ranges_m_twenties = [0, 4, 8, 10.6, 14.9, 18.7, 23.2, 58.6, 1]
bfp_ranges_m_thirties = [0, 4, 8, 14.6, 18.3, 21.4, 25, 58.6, 1]
bfp_ranges_m_forties = [0, 4, 8, 17.5, 20.7, 23.5, 26.7, 58.6, 1]
bfp_ranges_m_fifties = [0, 4, 8, 19.2, 22.2, 24.7, 27.9, 58.6, 1]
bfp_ranges_m_sixties = [0, 4, 8, 19.8, 22.7, 25.3, 28.5, 58.6, 1]

# Save male ranges
bfp_ranges_m = [bfp_ranges_m_twenties, bfp_ranges_m_thirties, bfp_ranges_m_forties, bfp_ranges_m_fifties, bfp_ranges_m_sixties]


# Generate data
age_groups = ['twenties', 'thirties', 'forties', 'fifties', 'sixties'] # for reference
sex_groups = ['female', 'male'] # for reference

# FEMALE
bfp_f = []
scores_f = []
ages_f = []
sex_f = []
grade_f = []

for age_group_i, age_group in enumerate(bfp_ranges_f):
    age = age_groups[age_group_i]
    for grade, bfp_group in enumerate(age_group):
        # Set scores
        if grade == 0:
            scores = 0      # Unhumanly low
        elif grade == 1:
            scores = 0.3    # Low (increased health risk)
        elif grade == 2:
            scores = 1      # Excellent/Fit
        elif grade == 3:
            scores = 1      # Good/Normal
        elif grade == 4:
            scores = 0.9    # Fair/Average
        elif grade == 5:
            scores = 0.7    # Poor (increased health risk)
        elif grade == 6:
            scores = 0.3    # High (increased health risk)
        elif grade == 7:
            scores = 0      # Unhumanly high
        elif grade == 8:
            scores = 0      # Unhumanly high (max)

        bfp_f.append(bfp_group)
        scores_f.append(scores)
        ages_f.append(age_group_i)
        sex_f.append(1)
        grade_f.append(grade)

female_data = pd.DataFrame(list(zip(bfp_f, scores_f, ages_f, sex_f, grade_f)), columns=['bfp', 'score', 'age', 'sex', 'grade'])

# MALE
bfp_m = []
scores_m = []
ages_m = []
sex_m = []
grade_m = []

for age_group_i, age_group in enumerate(bfp_ranges_m):
    age = age_groups[age_group_i]
    for grade, bfp_group in enumerate(age_group):
        # Set scores
        if grade == 0:
            scores = 0      # Unhumanly low
        elif grade == 1:
            scores = 0.3    # Low (increased health risk)
        elif grade == 2:
            scores = 1      # Excellent/Fit
        elif grade == 3:
            scores = 1      # Good/Normal
        elif grade == 4:
            scores = 0.9    # Fair/Average
        elif grade == 5:
            scores = 0.7    # Poor (increased health risk)
        elif grade == 6:
            scores = 0.3    # High (increased health risk)
        elif grade == 7:
            scores = 0      # Unhumanly high
        elif grade == 8:
            scores = 0      # Unhumanly high (max)

        bfp_m.append(bfp_group)
        scores_m.append(scores)
        ages_m.append(age_group_i)
        sex_m.append(0)
        grade_m.append(grade)

male_data = pd.DataFrame(list(zip(bfp_m, scores_m, ages_m, sex_m, grade_m)), columns=['bfp', 'score', 'age', 'sex', 'grade'])

# Combine female and male dataframes
df = pd.concat([female_data, male_data], axis=0).reset_index(drop=True)

# Save generated data to csv
df.to_csv('./../../data/processed/scoring_data.csv', index=False)


