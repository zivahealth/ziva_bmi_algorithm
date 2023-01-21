Ziva Health Baseline Health Score Algorithm
==============================

An algorithm that takes a user's height, weight, age, sex at birth, and waist circumference to return a baseline health score.

## Data
The data is downloaded and organized from [NHANES](https://wwwn.cdc.gov/nchs/nhanes/Default.aspx), a large source of health data provided by the CDC.

For the years 1999-2006, the downloaded data are organized in the following structure (with directory names `NHANES_1999-2000`, `NHANES_2001-2002`, `NHANES_2003-2004`, `NHANES_2005-2006`):

    ├── data/raw/NHANES_yyyy-yyyy
    │   ├── Demographics
    |   |   └── DEMO.XPT    <- Demographics data
    |   |
    │   ├── Examination
    |   |   ├── BMX.XPT     <- Body measurement data
    |   |   └── dxx.xpt     <- Dual Energy X-ray Absorptiometry (DXA) multiple imputation data
    |   |
    │   └── Questionnaire
    |       ├── SMQ.XPT     <- Smoking and tobacco use data
    |       ├── SMQFAM.XPT  <- Household smoking and tobacco use data
    |       └── SMQMEC.XPT  <- Recent smoking and tobacco use data
    
For `NHANES_2017-Mar2020`, the data follow the same structure, but there is no DXA data, instead of `SMQMEC.XPT` there is `SMQRTU.XPT`, and there is an additional file `SMQSHS.XPT` for secondhand smoke exposure. Because the data from 2017-2020 do not include DXA data, we disregard it for this project. `~/src/data/01-convert_to_csv.py` converts all of the datasets from XPT to CSV, storing them in the same location. `~/src/data/02-data_cleaning.py` cleans the raw CSV files, resulting in the datasets found in `~/data/processed/`. See `~/notebooks/01-data_prep.ipynb` and `~/notebooks/01-eda.ipynb`, which were written concurrently, for more information about this process.



Project Organization
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


