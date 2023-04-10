# Import packages
import numpy as np
import pandas as pd
import os
import pickle
from sklearn.ensemble import RandomForestRegressor
from main_run_algorithm import outlier_detection, read_models, score_bfp


class BMIService:
    def get_m(self, weight_kg=0, height_cm=0, sex_num=0, age_yrs=0, waist_circum_cm=0):
        models = read_models()
        # Get user info
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
            grade_feedback = "Your predicted body fat is very high and may signify health complications."
        else:
            grade_feedback = "Your predicted body fat is unhumanly high. Please double check your input measurements."

        # Identify outliers
        outlier_output = outlier_detection(user_data)

        body_fat_pred_per = np.round(body_fat_pred, 2)
        health_score_per = np.round(score * 100, 2)

        # Construct output string (02/15/2023: Omitting feedback message)
        output = """Predicted body fat percentage: {}%
        Health score: {}%
    {}""".format(
            np.round(body_fat_pred, 2), np.round(score * 100, 2), outlier_output
        )

        # Report results
        # print(output)
        # print(grade_feedback)
        return {
            "output": output,
            "body_fat_pred_per": body_fat_pred_per,
            "health_score_per": health_score_per,
            "grade_feedback": grade_feedback,
        }

    def get_i(self, weight_lbs, height_in, sex_num, age_yrs, waist_circum_in):
        models = read_models()
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
            grade_feedback = "Your predicted body fat is very high and may signify health complications."
        else:
            grade_feedback = "Your predicted body fat is unhumanly high. Please double check your input measurements."

        # Identify outliers
        outlier_output = outlier_detection(user_data)

        # Construct output string (02/15/2023: Omitting feedback message)
        health_score_per = np.round(score * 100, 2)
        body_fat_pred_per = np.round(body_fat_pred, 2)
        output = """Predicted body fat percentage: {}%
            Health score: {}%
        {}""".format(
            np.round(body_fat_pred, 2), np.round(score * 100, 2), outlier_output
        )
        # Report results
        # print(output)
        # print(grade_feedback)
        return {
            "output": output,
            "body_fat_pred_per": body_fat_pred_per,
            "health_score_per": health_score_per,
            "grade_feedback": grade_feedback,
        }


# if __name__ == "__main__":
#     bmi = BMIService()
#     output= bmi.get_m(140, 1.82, 1, 25, 71)
#     print({"bmi": output})
