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
    models_path = "./../../models/rf_regressors/"
    models = []

    for file in os.listdir(models_path):
        # Save model
        with open(models_path + file, "rb") as m:
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
    if weight_unit == "m":
        # Prompt for weight
        weight_kg = input("Enter weight (kg): ")

        # Prompt for height
        height_m = input("""Enter height (m) """)
        # Calculate precise height
        height_cm = float(height_m) * 100

        # Prompt for sex
        sex = input("Enter sex at birth: (m/f) ")
        sex_num = 1 if sex == "f" else 0

        # Prompt for age
        age_yrs = input("Enter age: ")

        # Prompt for waist circumference
        waist_circum_cm = input("Enter waist circumference (cm): ")

        # Save data in numpy array to return
        user_data = np.array(
            [
                [
                    float(weight_kg),
                    float(height_cm),
                    float(sex_num),
                    float(age_yrs),
                    float(waist_circum_cm),
                ]
            ]
        )

        return user_data

    # Prompt user for data in imperial system
    elif weight_unit == "i":
        # Prompt for weight
        weight_lbs = input("Enter weight (lbs): ")

        # Prompt for height
        height_input = input(
            """Enter height in feet and inches (for example, enter 5'10" as 5 10) """
        ).split()
        # Calculate precise height
        height_in = float(height_input[0]) * 12 + float(height_input[1])

        # Prompt for sex
        sex = input("Enter sex at birth: (m/f) ")
        sex_num = 1 if sex == "f" else 0

        # Prompt for age
        age_yrs = input("Enter age: ")

        # Prompt for waist circumference
        waist_circum_in = input("Enter waist circumference (inches): ")

        # Save data in numpy array to return
        user_data = np.array(
            [
                [
                    float(weight_lbs),
                    float(height_in),
                    float(sex_num),
                    float(age_yrs),
                    float(waist_circum_in),
                ]
            ]
        )

        return user_data * CONVERSION_ARRAY

    # Error
    else:
        print("Error: not recognized")
        quit()


def score_bfp(bfp, age, sex_num):
    """
    Construct the scoring algorithm from "~/models/lm_poly7_coeffs.csv" and calculate
    the health score

    Returns:
        A tuple, [0]the health score between 0 and 1, [1]a message based on the grade
    """
    # Determine age class
    if age < 30:
        age_class = 0
    elif age < 40:
        age_class = 1
    elif age < 50:
        age_class = 2
    elif age < 60:
        age_class = 3
    else:
        age_class = 4

    # Read in scoring data
    interp_pts = pd.read_csv("./../../data/processed/scoring_data.csv")

    # Subset based on age and sex
    iterp_pts_sub = interp_pts[
        (interp_pts["age"] == age_class) & (interp_pts["sex"] == sex_num)
    ].copy()

    # Convert columns of interest to lists
    bfp_range = iterp_pts_sub["bfp"].tolist()
    score_range = iterp_pts_sub["score"].tolist()
    grade_range = iterp_pts_sub["grade"].tolist()

    # Interpolate health score
    health_score = np.interp(bfp, bfp_range, score_range)
    grade_output = np.floor(np.interp(bfp, bfp_range, grade_range))

    return (health_score, grade_output)


def outlier_detection(user_input):
    """
    Check the user input for values that lie outside the ranges of data featured in the
    NHANES dataset. Warn the user that there may be inaccuracies in their results because
    of these outliers.

    Returns: A tuple, [0]the message associated with rounding age outliers to the nearest
    age range for the scoring algorithm, [1]the message associated with any outliers to
    the ranges present in the NHANES data.
    """
    # Initialize tracking of outliers
    outliers = []
    # Initialize tracking of age (for scoring algorithm limitations per http://pennshape.upenn.edu/files/pennshape/Body-Composition-Fact-Sheet.pdf)
    age_note = ""

    # Initialize forms to fill in potential outlier information
    outliers_note_form = "NOTE: We detected outliers in the following {} you entered: {}. Please be aware that this may affect the accuracy of your predicted body fat percentage and subsequent health score."
    age_note_form = "NOTE: Due to limitations in research data, our health score is most accurate for individuals between the ages of 20 and 69. Because you fall {} this range, your health score is based on healthy body fat percentage ranges of individuals aged {}, and may therefore contain inaccuracies."

    # Identify outliers
    if user_input[0][0] < 18.5 or user_input[0][0] > 218.6:
        outliers.append("weight")
    if user_input[0][1] < 110 or user_input[0][1] > 200:
        outliers.append("height")
    if user_input[0][3] < 8 or user_input[0][3] > 85:
        outliers.append("age")
    if user_input[0][4] < 32 or user_input[0][4] > 175:
        outliers.append("waist circumference")

    # Format outliers note
    if len(outliers) == 0:
        outliers_note = ""
    elif len(outliers) == 1:
        outliers_note = outliers_note_form.format("measurement", ", ".join(outliers))
    else:
        outliers_note = outliers_note_form.format("measurements", ", ".join(outliers))

    # Format age note
    if user_input[0][3] < 20:
        age_note = age_note_form.format("under", "20-29")
    elif user_input[0][3] > 69:
        age_note = age_note_form.format("above", "60-69")

    # Format the final output string to include a newline if both messages contain text
    if len(age_note) == 0:
        return outliers_note
    elif len(outliers_note) == 0:
        return age_note
    else:
        return outliers_note + "\n" + age_note


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

    # Generate the score and grade
    score, grade = score_bfp(body_fat_pred, user_data[0][3], user_data[0][2])

    # Identify proper feedback based on grade

    # 02/15/2023: As it stands, Parveen requested that we omit the feedback messages and let the users interpret their
    # health score themselves. I will leave the code for generating the grade feedback for potential future use, even though
    # it is obsolete in this iteration of the project

    if grade == 0:
        grade_feedback = "Your predicted body fat percentage is unhumanly low. Please double check your input measurements."
    elif grade == 1:
        grade_feedback = "Your predicted body fat percentage is very low and may signify health complications."
    elif grade == 2 or grade == 3 or grade == 4:
        grade_feedback = "Your predicted body fat is in the ideal range."
    elif grade == 5 or grade == 6:
        grade_feedback = (
            "Your predicted body fat is very high and may signify health complications."
        )
    else:
        grade_feedback = "Your predicted body fat is unhumanly high. Please double check your input measurements."

    # Identify outliers
    outlier_output = outlier_detection(user_data)

    # Construct output string (02/15/2023: Omitting feedback message)
    output = """Predicted body fat percentage: {}%
    Health score: {}%
{}""".format(
        np.round(body_fat_pred, 2), np.round(score * 100, 2), outlier_output
    )

    # Report results
    print(output)
