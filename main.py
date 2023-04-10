from typing import Annotated
from fastapi import FastAPI, Form
from service import BMIService
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    bmi = BMIService()
    weight_kg = 140
    height_cm = 1.82
    sex_num = 1
    age_yrs = 25
    waist_circum_cm = 71
    output1 = bmi.get_m(weight_kg, height_cm, sex_num, age_yrs, waist_circum_cm)
    weight_lbs = 140
    height_in = 72
    sex_num = 1  # m=1|f=0
    age_yrs = 25
    waist_circum_in = 28
    output = bmi.get_i(weight_lbs, height_in, sex_num, age_yrs, waist_circum_in)
    return {"bmi": output, "bmi-m": output1}


@app.post("/bmi")
def calculate_bmi(
    metricSystem: Annotated[str, Form()],
    age: Annotated[int, Form()],
    gender: Annotated[int, Form()],
    heightInFt: Annotated[int, Form()],
    heightInM: Annotated[int, Form()],
    weightInKG: Annotated[int, Form()],
    waistCircumCm: Annotated[int, Form()],
):
    print("age: ", age)
    print("gender: ", gender)
    heightInCm = heightInFt
    print("heightInFt: ", heightInFt)
    bmi = BMIService()
    if metricSystem == "metric":
        weight_kg = weight_kg
        height_cm = heightInCm
        sex_num = gender
        age_yrs = age
        waist_circum_cm = waistCircumCm
        output1 = bmi.get_m(weight_kg, height_cm, sex_num, age_yrs, waist_circum_cm)
    else:
        weight_lbs = weight_kg * 2.205
        height_in = heightInCm / 2.54
        sex_num = gender  # m=0|f=1
        age_yrs = age
        waist_circum_in = waist_circum_in
        output = bmi.get_i(weight_lbs, height_in, sex_num, age_yrs, waist_circum_in)
    return {"bmi": output, "bmi-m": output1}
