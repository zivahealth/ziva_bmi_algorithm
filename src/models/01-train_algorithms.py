### IMPORT MODULES ###
import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor


### DATA PREP ###
data = []

for i in range(1, 6):
    data_i = pd.read_csv("./../../data/processed/M" + str(i) + "_data.csv").set_index('id')
    data.append(data_i)

# Fill lists with NaN values so they can be indexed
X_train = np.repeat(np.nan, 5).tolist()
X_test = np.repeat(np.nan, 5).tolist()
y_train = np.repeat(np.nan, 5).tolist()
y_test = np.repeat(np.nan, 5).tolist()

# Split by same ids for all imputations
predictors_cols = ['weight_kg', 'height_cm', 'sex', 'age_yrs', 'waist_circum_cm']

for i, data_i in enumerate(data):
    X_train[i], X_test[i], y_train[i], y_test[i] = train_test_split(
        np.array(data_i[predictors_cols]),
        np.array(data_i['total_fat_pct']),
        test_size=0.3,
        random_state=42
    )
    

### ALGORITHM LEARNING ###
# Initialize
model_rf = np.repeat(RandomForestRegressor(max_depth=10, random_state=42), 5).tolist() # The best tree depth seems to be 10

# Train
for i, model_i in enumerate(model_rf):
    model_i.fit(X_train[i], y_train[i])

### SAVE ALGORITHMS ###
for i, model_i in enumerate(model_rf):
    with open('./../../models/rf_regressors/model' + str(i+1) + '.pkl', 'wb') as f:
        pickle.dump(model_i, f)