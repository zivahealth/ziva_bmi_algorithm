# A script for generating simulated data to reflect the desired behavior of the scoring algorithm

# Install packages
import numpy as np
import pandas as pd

# Define ranges
bfp_ranges_f_twenties = [
    np.arange(0, 9.4, 0.1),
    np.arange(9.5, 13.9, 0.1),
    np.arange(14, 16.5, 0.1),
    np.arange(16.6, 19.4, 0.1),
    np.arange(19.5, 22.7, 0.1),
    np.arange(22.8, 27.1, 0.1),
    np.arange(27.2, 58.5, 0.1),
    np.arange(58.6, 70, 0.1)
]

bfp_ranges_f_thirties = [
    np.arange(0, 9.4, 0.1),
    np.arange(9.5, 13.9, 0.1),
    np.arange(14, 17.4, 0.1),
    np.arange(17.5, 20.8, 0.1),
    np.arange(20.9, 24.6, 0.1),
    np.arange(24.7, 29.1, 0.1),
    np.arange(29.2, 58.5, 0.1),
    np.arange(58.6, 70, 0.1)
]

bfp_ranges_f_forties = [
    np.arange(0, 9.4, 0.1),
    np.arange(9.5, 13.9, 0.1),
    np.arange(14, 19.8, 0.1),
    np.arange(19.9, 23.8, 0.1),
    np.arange(23.9, 27.6, 0.1),
    np.arange(27.7, 31.9, 0.1),
    np.arange(32, 58.5, 0.1),
    np.arange(58.6, 70, 0.1)
]

bfp_ranges_f_fifties = [
    np.arange(0, 9.4, 0.1),
    np.arange(9.5, 13.9, 0.1),
    np.arange(14, 22.5, 0.1),
    np.arange(22.6, 27, 0.1),
    np.arange(27.1, 30.4, 0.1),
    np.arange(30.5, 34.5, 0.1),
    np.arange(34.6, 58.5, 0.1),
    np.arange(58.6, 70, 0.1)
]

bfp_ranges_f_sixties = [
    np.arange(0, 9.4, 0.1),
    np.arange(9.5, 13.9, 0.1),
    np.arange(14, 23.2, 0.1),
    np.arange(23.3, 27.9, 0.1),
    np.arange(28, 31.3, 0.1),
    np.arange(31.4, 35.4, 0.1),
    np.arange(35.5, 58.5, 0.1),
    np.arange(58.6, 70, 0.1)
]

# Save female ranges
bfp_ranges_f = [bfp_ranges_f_twenties, bfp_ranges_f_thirties, bfp_ranges_f_forties, bfp_ranges_f_fifties, bfp_ranges_f_sixties]

bfp_ranges_m_twenties = [
    np.arange(0, 4, 0.1),
    np.arange(4, 7.9, 0.1),
    np.arange(8, 10.5, 0.1),
    np.arange(10.6, 14.8, 0.1),
    np.arange(14.9, 18.6, 0.1),
    np.arange(18.7, 23.1, 0.1),
    np.arange(23.2, 58.5, 0.1),
    np.arange(58.6, 70, 0.1)
]

bfp_ranges_m_thirties = [
    np.arange(0, 4, 0.1),
    np.arange(4, 7.9, 0.1),
    np.arange(8, 14.5, 0.1),
    np.arange(14.6, 18.2, 0.1),
    np.arange(18.3, 21.3, 0.1),
    np.arange(21.4, 24.9, 0.1),
    np.arange(25, 58.5, 0.1),
    np.arange(58.6, 70, 0.1)
]

bfp_ranges_m_forties = [
    np.arange(0, 4, 0.1),
    np.arange(4, 7.9, 0.1),
    np.arange(8, 17.4, 0.1),
    np.arange(17.5, 20.6, 0.1),
    np.arange(20.7, 23.4, 0.1),
    np.arange(23.5, 26.6, 0.1),
    np.arange(26.7, 58.5, 0.1),
    np.arange(58.6, 70, 0.1)
]

bfp_ranges_m_fifties = [
    np.arange(0, 4, 0.1),
    np.arange(4, 7.9, 0.1),
    np.arange(8, 19.1, 0.1),
    np.arange(19.2, 22.1, 0.1),
    np.arange(22.2, 24.6, 0.1),
    np.arange(24.7, 27.8, 0.1),
    np.arange(27.9, 58.5, 0.1),
    np.arange(58.6, 70, 0.1)
]

bfp_ranges_m_sixties = [
    np.arange(0, 4, 0.1),
    np.arange(4, 7.9, 0.1),
    np.arange(8, 19.7, 0.1),
    np.arange(19.8, 22.6, 0.1),
    np.arange(22.7, 25.2, 0.1),
    np.arange(25.3, 28.4, 0.1),
    np.arange(28.5, 58.5, 0.1),
    np.arange(58.6, 70, 0.1)
]

# Save male ranges
bfp_ranges_m = [bfp_ranges_m_twenties, bfp_ranges_m_thirties, bfp_ranges_m_forties, bfp_ranges_m_fifties, bfp_ranges_m_sixties]


# Generate data
age_groups = ['twenties', 'thirties', 'forties', 'fifties', 'sixties']

# FEMALE
bfp_f = []
scores_f = []
ages_f = []
sex_f = []

for age_group_i, age_group in enumerate(bfp_ranges_f):
    age = age_groups[age_group_i]
    for grade, bfp_group in enumerate(age_group):
        n_group = len(bfp_group)

        # Set scores
        if grade == 0:
            scores = np.arange(0, .3, (.3-0)/n_group)
        elif grade == 1:
            scores = np.arange(.3, .9, (.9-.3)/n_group)
        elif grade == 2:
            scores = np.arange(.9, 1, (1-.9)/n_group)
        elif grade == 3:
            scores = np.arange(1, .8, (.8-1)/n_group)
        elif grade == 4:
            scores = np.arange(.8, .7, (.7-.8)/n_group)
        elif grade == 5:
            scores = np.arange(.7, .6, (.6-.7)/n_group)
        elif grade == 6:
            scores = np.arange(.6, .3, (.3-.6)/n_group)
        elif grade == 7:
            scores = np.arange(.3, 0, (0-.3)/n_group)

        for i, obs in enumerate(bfp_group):
            bfp_f.append(obs)
            scores_f.append(scores[i])
            ages_f.append(age)
            sex_f.append("f")

female_data = pd.DataFrame(list(zip(bfp_f, scores_f, ages_f, sex_f)), columns=['bfp', 'score', 'age', 'sex'])

# MALE
bfp_m = []
scores_m = []
ages_m = []
sex_m = []

for age_group_i, age_group in enumerate(bfp_ranges_m):
    age = age_groups[age_group_i]
    for grade, bfp_group in enumerate(age_group):
        n_group = len(bfp_group)

        # Set scores
        if grade == 0:
            scores = np.arange(0, .3, (.3-0)/n_group)
        elif grade == 1:
            scores = np.arange(.3, .9, (.9-.3)/n_group)
        elif grade == 2:
            scores = np.arange(.9, 1, (1-.9)/n_group)
        elif grade == 3:
            scores = np.arange(1, .8, (.8-1)/n_group)
        elif grade == 4:
            scores = np.arange(.8, .7, (.7-.8)/n_group)
        elif grade == 5:
            scores = np.arange(.7, .6, (.6-.7)/n_group)
        elif grade == 6:
            scores = np.arange(.6, .3, (.3-.6)/n_group)
        elif grade == 7:
            scores = np.arange(.3, 0, (0-.3)/n_group)

        for i, obs in enumerate(bfp_group):
            bfp_m.append(obs)
            scores_m.append(scores[i])
            ages_m.append(age)
            sex_m.append("m")

male_data = pd.DataFrame(list(zip(bfp_m, scores_m, ages_m, sex_m)), columns=['bfp', 'score', 'age', 'sex'])

# Combine female and male dataframes
df = pd.concat([female_data, male_data], axis=0).reset_index(drop=True)

# Save generated data to csv
df.to_csv('./../../data/processed/scoring_data.csv', index=False)


