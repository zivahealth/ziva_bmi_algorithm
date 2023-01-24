Ziva Health Baseline Health Score Algorithm
==============================

An algorithm that takes a user's height, weight, age, sex at birth, and waist circumference to return a baseline health score.

Setup
------------
This project uses Anaconda as a package manager. With Anaconda installed on your machine, run `conda env create -f environment.yml` to create a virtual environment with all the necessary dependencies.

Project Breakdown
------------
## Data
The data is downloaded and organized from [NHANES](https://wwwn.cdc.gov/nchs/nhanes/Default.aspx), a large source of health data provided by the CDC.

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

## Algorithm
This project uses a random forest algorithm.

File Structure
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------


