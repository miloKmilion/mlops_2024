#!/usr/bin/env python
# coding: utf-8

# ### This is the notebook for the batch offline deployment
# Additionally, the model will be used to score. 

# In[42]:


import pickle
import os
import pandas as pd
import uuid
import sys

from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

from sklearn.pipeline import make_pipeline

import mlflow



mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("green-taxi-duration")


# In[53]:


def generate_uuids(n):
    ride_ids = []
    for i in range(n):
        ride_ids.append(str(uuid.uuid4()))
    return ride_ids

def read_dataframe(filename: str):
    df = pd.read_parquet(filename)

    df['duration'] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df.duration = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)]
    
    df['ride_id'] = generate_uuids(len(df))

    return df


def prepare_dictionaries(df: pd.DataFrame):
    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)
    
    df['PU_DO'] = df['PULocationID'] + '_' + df['DOLocationID']

    categorical = ['PU_DO']
    numerical = ['trip_distance']
    dicts = df[categorical + numerical].to_dict(orient='records')
    return dicts


# In[60]:


# In this case we dont have train and test data, just the data to which the model will be applied. 
def load_model(run_id):
    logged_model =f's3://mlopsbatch/1/{run_id}/artifacts/model'
    model = mlflow.pyfunc.load_model(logged_model)
    return model


def apply_model(input_file, run_id, output_file):

    df = read_dataframe(input_file)
    dicts = prepare_dictionaries(df)

    
    model = load_model(run_id)
    y_pred = model.predict(dicts)

    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['lpep_pickup_datetime'] = df['lpep_pickup_datetime']
    df_result['PULocationID'] = df['PULocationID']
    df_result['DOLocationID'] = df['DOLocationID']
    df_result['actual_duration'] = df['duration']
    df_result['predicted_duration'] = y_pred
    df_result['diff'] = df_result['actual_duration'] - df_result['predicted_duration']
    df_result['model_version'] = run_id
    

    df_result.to_parquet(output_file, index=False)


# In[61]:

def run():
    year = int(sys.argv[2]) # 2021
    month = int(sys.argv[3]) # 2
    taxi_type = sys.argv[1] # 'green'

    INPUT_FILE = f'https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet'
    #INPUT_FILE = f'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2021-01.parquet'
    OUTPUT_FILE = f'output/{taxi_type}/{year:04d}-{month:02d}.parquet'
    RUN_ID = os.getenv('RUN_ID', '250694a4d07240ec8858323e6590c050')

    apply_model(input_file=INPUT_FILE, run_id=RUN_ID, output_file=OUTPUT_FILE)

if __name__ == '__main__':
    run()





