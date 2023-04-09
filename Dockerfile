# Initialize anaconda image
FROM continuumio/anaconda3

# Set working directory as /app
WORKDIR /app

# Install necessary packages
RUN conda install numpy=1.21.5 pandas=1.4.4 scikit-learn=1.1.1
RUN pip install fastapi==0.95.0
RUN pip install fastapi[all]
RUN pip install "unicorn[standard]"
# Copy all necessary files from src/models/essential_files.zip
COPY data/processed/scoring_data.csv /app/data/processed/
COPY models/rf_regressors/ /app/models/rf_regressors
COPY src/models/02-run_algorithm.py /app/src/models/02-run_algorithm.py
COPY main.py /app/src/models/main.py
COPY start.sh /app/src/models/start.sh

# Navigate to src/models/ in order to run the algorithm script
WORKDIR /app/src/models/

# Run the script to query the user's information and return a health score / predicted body fat pct
# CMD [ "python3", "02-run_algorithm.py" ]

CMD [ "unicorn", "main:app", "--reload" ]
