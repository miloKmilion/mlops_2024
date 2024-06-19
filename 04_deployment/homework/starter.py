#!/usr/bin/env python
# coding: utf-8
import pickle
import pandas as pd
import numpy as np
import sys
import os

#* Opening the model. 
with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)

# Selecting the categorical variables
categorical = ['PULocationID', 'DOLocationID']


def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    standard_deviation_calc = np.std(df['duration'])
    print(f"The standard deviation of the calculated trip duration is: {standard_deviation_calc}")
        
    return df

#df = read_data(INPUT_FILE)
#df.head()


def apply_model(input_file, year, month, output_file):

    df = read_data(input_file)
    dicts = df[categorical].to_dict(orient='records')
    
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)
    print(f'The standard deviation of the predicted: {np.std(y_pred)}')
    print(f'The mean of the predicted: {np.mean(y_pred)}')

    
    df_result = pd.DataFrame()
    df_result['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
    df_result['predicted_duration'] = y_pred
    
    df_result.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False
        )
    
    file_size = os.path.getsize(output_file)
    file_size_mb = file_size / (1024 * 1024)  # size in megabytes
    print(f'The len of the output file is: {len(df_result)}')
    print(f"The size of the Parquet file is {file_size_mb:.2f} MB.")
    

def run():
    year = int(sys.argv[2]) # 2021
    month = int(sys.argv[3]) # 2
    taxi_type = sys.argv[1] # 'green'

    INPUT_FILE = f'https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet'
    #INPUT_FILE = f'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2021-01.parquet'
    OUTPUT_FILE = f'output/{taxi_type}-{year:04d}-{month:02d}.parquet'
    
    apply_model(input_file=INPUT_FILE, year=year, month=month, output_file=OUTPUT_FILE)

if __name__ == '__main__':
    run()