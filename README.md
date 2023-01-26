# Ziva Health Baseline Health Score Algorithm

An algorithm that takes a user's height, weight, age, sex at birth, and waist circumference to return a baseline health score.

## Setup for Replication
This project uses Anaconda as a package manager. With Anaconda installed on your machine, run `conda env create -f environment.yml` to create a virtual environment with all the necessary dependencies.

## Data
The data is downloaded and organized from [NHANES](https://wwwn.cdc.gov/nchs/nhanes/Default.aspx), a large source of health data provided by the CDC.

### Retrieval and Organization
For the years 1999-2006, the downloaded data are organized in the following structure [here](./data/raw/) (with directory names `NHANES_1999-2000`, `NHANES_2001-2002`, `NHANES_2003-2004`, `NHANES_2005-2006`):

    ├── data/raw/NHANES_yyyy-yyyy
    │   ├── Demographics
    │   │   └── DEMO.XPT    <- Demographics data
    │   │
    │   ├── Examination
    │   │   ├── BMX.XPT     <- Body measurement data
    │   │   └── dxx.xpt     <- Dual Energy X-ray Absorptiometry (DXA) multiple imputation data
    │   │
    │   └── Questionnaire
    │       ├── SMQ.XPT     <- Smoking and tobacco use data
    │       ├── SMQFAM.XPT  <- Household smoking and tobacco use data
    │       └── SMQMEC.XPT  <- Recent smoking and tobacco use data

We did not use the household smoking and tobacco use nor the recent smoking and tobacco use datasets. To view the documentation for the datasets we used in this project, access the links below:
- Demographics: [1999-2000](https://wwwn.cdc.gov/Nchs/Nhanes/1999-2000/DEMO.htm), [2001-2002](https://wwwn.cdc.gov/Nchs/Nhanes/2001-2002/DEMO_B.htm), [2003-2004](https://wwwn.cdc.gov/Nchs/Nhanes/2003-2004/DEMO_C.htm), [2005-2006](https://wwwn.cdc.gov/Nchs/Nhanes/2005-2006/DEMO_D.htm)
- Body measurements: [1999-2000](https://wwwn.cdc.gov/Nchs/Nhanes/1999-2000/BMX.htm), [2001-2002](https://wwwn.cdc.gov/Nchs/Nhanes/2001-2002/BMX_B.htm), [2003-2004](https://wwwn.cdc.gov/Nchs/Nhanes/2003-2004/BMX_C.htm), [2005-2006](https://wwwn.cdc.gov/Nchs/Nhanes/2005-2006/BMX_D.htm)
- DXA: [1999-2006](https://wwwn.cdc.gov/Nchs/Nhanes/Dxa/Dxa.aspx)
- Smoking and tobacco use: [1999-2000](https://wwwn.cdc.gov/Nchs/Nhanes/1999-2000/SMQ.htm), [2001-2002](https://wwwn.cdc.gov/Nchs/Nhanes/2001-2002/SMQ_B.htm), [2003-2004](https://wwwn.cdc.gov/Nchs/Nhanes/2003-2004/SMQ_C.htm), [2005-2006](https://wwwn.cdc.gov/Nchs/Nhanes/2005-2006/SMQ_D.htm)
    
The `NHANES_2017-Mar2020` directory follows the same general structure as shown above, but with the following exceptions:

- There is no DXA data
- Instead of `SMQMEC.XPT` there is `SMQRTU.XPT`
- There is an additional file `SMQSHS.XPT` for secondhand smoke exposure

Because the data from 2017-2020 do not include DXA data, we disregard it for this project. [01-convert_to_csv.py](./src/data/01-convert_to_csv.py) converts all of the datasets from XPT to CSV, storing them alongside the XPT files in [data/raw](./data/raw/). [02-data_cleaning.py](./src/data/02-data_cleaning.py) cleans the raw CSV files, resulting in the final datasets found in [data/processed](./data/processed/). See [01-eda.ipynb](./notebooks/01-eda.ipynb) for more information about this process.

### Multiple Imputation for DXA Data

### Data Thresholds
The participants in the NHANES held demographics/measurements in the following ranges:
|         | Weight (kg/lbs)  | Height (m/ft-in)  | Age   | Waist Circumference  |
| :-----: | ---------------- | ----------------- | ----- | -------------------- |
| Minimum | value            | value             | value | value                |
| Maximum | value            | value             | value | value                |

Because the algorithm is not trained on any data that exceed these thresholds, we rely on the algorithm to generate an accurate score for individuals outside of these ranges.

## Algorithm
This project uses a random forest algorithm to predict the user's body fat percentage, which is then fed into a polynomial regression model to return a health score between 0 and 1.

We built this polynomial regression algorithm using [this](http://pennshape.upenn.edu/files/pennshape/Body-Composition-Fact-Sheet.pdf) information about healthy body fat percentages.

### Scoring Mechanism
| Body Fat Percentage Group         | Scoring Range |
| :-------------------------------: | ------------- |
| Unhumanly Low                     | 0-30%         |
| Low (Increased Health Risk)       | 30-90%        |
| Excellent/Fit (Healthy)           | 90-100%       |
| Good/Normal (Healthy)             | 80-100%       |
| Fair/Average (Healthy)            | 70-80%        |
| Poor (Increased Health Risk)      | 60-70%        |
| High (Increased Health Risk)      | 30-60%        |
| Unhumanly High                    | 0-30%         |

## File Structure

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── models             <- Saved random forest models (one for each imputation) as pickle
    │                         files.
    │
    ├── notebooks          <- Jupyter notebooks.
    │
    ├── references         <- Research articles informing the baseline algorithms.
    │
    ├── reports            <- Jupyter notebook outputs, saved as HTML and PDF files.
    │
    ├── requirements.txt   <- The yaml file for reproducing the analysis environment, e.g.
    │                         generated with `conda env export > environment.yml`
    │
    └── src                <- Source code for use in this project.
        ├── data           <- Scripts to convert XPT datasets to CSV, clean data
        │   ├── 01-convert_to_csv.py
        │   └── 02-data_cleaning.py
        │
        └── models         <- Scripts to train and save the algorithm
            └── 01-train_algorithm.py