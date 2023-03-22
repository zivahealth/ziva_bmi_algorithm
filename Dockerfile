# Initialize anaconda image
FROM continuumio/anaconda3

# Set working directory as /app
WORKDIR /app

# Install necessary packages
RUN conda install numpy=1.21.5 pandas=1.4.4 scikit-learn=1.1.1

# Copy all necessary files from src/models/essential_files.zip
COPY data/processed/scoring_data.csv /app/data/processed/
COPY models/rf_regressors/ /app/models/rf_regressors
COPY src/models/02-run_algorithm.py /app/src/models/02-run_algorithm.py

# Navigate to src/models/ in order to run the algorithm script
WORKDIR /app/src/models/

# Run the script to query the user's information and return a health score / predicted body fat pct
CMD [ "python3", "02-run_algorithm.py" ]