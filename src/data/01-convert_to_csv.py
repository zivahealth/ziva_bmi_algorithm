# Import packages
import pandas as pd
import os
from warnings import simplefilter

# Suppress PerformanceWarnings (see https://stackoverflow.com/questions/75189574/pandas-pd-read-sas-returns-performancewarning-dataframe-is-highly-fragmented)
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

# Set root directory
rootdir = "./../../data/raw/"

# Cycle through all files
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        # Filter out non XPT files
        if file.endswith(".XPT") | file.endswith(".xpt"):
            # Construct filepath
            filepath = os.path.join(subdir, file)
            
            # Read in XPT data
            data = pd.read_sas(filepath)

            # Construct new filepath
            newfile = file[:-3] + "csv"
            newfile_path = os.path.join(subdir, newfile)

            # Create directory if does not exist
            # Path(newsubdir).mkdir(parents=True, exist_ok=True)

            # Save dataset as csv
            data.to_csv(newfile_path, index=False)

            del data
            
            print(file, "successfully converted to", newfile)