# Import packages
import numpy as np
import pandas as pd
import os
import pickle
from sklearn.ensemble import RandomForestRegressor

# Define functions
def read_models():
    """
    Read in and save the Random Forest models from "~/models/".

    Returns:
        List of five sklearn RandomForestRegressor objects
    """

    # Read in models
    models_path = './../../models/rf_regressors/'
    models = []

    for file in os.listdir(models_path):
        # Save model
        with open(models_path + file, 'rb') as m:
            models.append(pickle.load(m))

    return models

def data_prompt():
    """
    Prompt the user for all necessary information to generate a baseline health score.

    Returns:
        2d numpy array consisting of one element in the first dimension and five
        elements in the second dimension: weight in kilograms, height in 
        centimeters, sex (1 for female, 0 for male), age in years, and waist 
        circumference in centimeters
    """

    CONVERSION_ARRAY = np.array([0.45359237, 2.53999862, 1, 1, 2.53999862])

    # Establish units of measure
    weight_unit = input("Do you prefer metric system or imperial system? (m/i) ")

    # Prompt user for data in metric system
    if weight_unit == 'm':
        # Prompt for weight
        weight_kg = input("Enter weight (kg): ")

        # Prompt for height
        height_m = input("""Enter height (m) """)
        # Calculate precise height
        height_cm = float(height_m) * 100

        # Prompt for sex
        sex = input("Enter sex at birth: (m/f) ")
        sex_num = 1 if sex == 'f' else 0

        # Prompt for age
        age_yrs = input("Enter age: ")

        # Prompt for waist circumference
        waist_circum_cm = input("Enter waist circumference (cm): ")

        # Save data in numpy array to return
        user_data = np.array([
            float(weight_kg),
            float(height_cm),
            float(sex_num),
            float(age_yrs),
            float(waist_circum_cm)
        ])

        return(user_data)

    # Prompt user for data in imperial system
    elif weight_unit == 'i':
        # Prompt for weight
        weight_lbs = input("Enter weight (lbs): ")

        # Prompt for height
        height_input = input("""Enter height in feet and inches (for example, enter 5'10" as 5 10) """).split()
        # Calculate precise height
        height_in = float(height_input[0]) * 12 + float(height_input[1])

        # Prompt for sex
        sex = input("Enter sex at birth: (m/f) ")
        sex_num = 1 if sex == 'f' else 0

        # Prompt for age
        age_yrs = input("Enter age: ")

        # Prompt for waist circumference
        waist_circum_in = input("Enter waist circumference (inches): ")

        # Save data in numpy array to return
        user_data = np.array([[
            float(weight_lbs),
            float(height_in),
            float(sex_num),
            float(age_yrs),
            float(waist_circum_in)
        ]])

        return(user_data * CONVERSION_ARRAY)

    # Error
    else:
        print("Error: not recognized")
        quit()


def score_bfp(bfp, age, sex_num):
    """
    Construct the scoring algorithm from "~/models/lm_poly7_coeffs.csv" and calculate the health score

    Returns:
        A float, the health score between 0 and 1.
    """

    # Determine age class
    if age < 30:
        age1 = 0
        age2 = 0
        age3 = 0
        age4 = 0
    elif age < 40:
        age1 = 1
        age2 = 0
        age3 = 0
        age4 = 0
    elif age < 50:
        age1 = 0
        age2 = 1
        age3 = 0
        age4 = 0
    elif age < 60:
        age1 = 0
        age2 = 0
        age3 = 1
        age4 = 0
    else:
        age1 = 0
        age2 = 0
        age3 = 0
        age4 = 1

    coefs = pd.read_csv("./../../models/lm_poly7_coeffs.csv")['x']

    health_score = np.sum([
        coefs[0],
        coefs[1] * bfp,
        coefs[2] * (bfp**2),
        coefs[3] * (bfp**3),
        coefs[4] * (bfp**4),
        coefs[5] * (bfp**5),
        coefs[6] * (bfp**6),
        coefs[7] * (bfp**7),
        coefs[8] * age1,
        coefs[9] * age2,
        coefs[10] * age3,
        coefs[11] * age4,
        coefs[12] * sex_num
    ])

    return(health_score)


if __name__ == "__main__":
    # Read in models
    models = read_models()

    # Get user info
    user_data = data_prompt()

    # Save body fat pct predictions for each imputation's model
    preds = []
    for m in models:
        preds.append(m.predict(user_data))

    # Average the five imputations to arrive at the predicted body fat percentage
    body_fat_pred = np.mean(preds)

    # Generate the score
    score = score_bfp(body_fat_pred, user_data[0][3], user_data[0][2])
    
    # Construct output string
    output = """Predicted body fat percentage: {}
    Health score: {}%""".format(np.round(body_fat_pred, 2), np.round(score, 2) * 100)

    # Report results
    print(output)

