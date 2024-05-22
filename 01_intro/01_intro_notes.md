### Notes Module 1.

#### Optional video: Training a ride duration prediction model

the data used is the yellow taxy data from the months january and february of 2023
https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet
https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-02.parquet


Remember notebooks are just for exploratory analysis and not final code. Is good to test parameters and models but creqating modular code is better. 

#### Separating the steps implemented we have:
    1. Load and Create dataset
    2. Vectorize the dataset into feature matrices: 
        IMPORTANT: We used a dict vectorization for this step but the vit_transform() function is only applied to the train data. The validation only uses the values in the 
        initial vectorization and apply the transform() function. This to maintain the number of features. 
    3. Train the model

The conjunction of those steps are the initial ML pipeline. 
By creatinf a pipeline.py parametrizing the values for training and testing. 

The output of the pipeline is a mature model. That is encapsuled in a ML service or web service. The user communicates with the service where the performance is monitores. 
An additional module is created to represent the monitoring of the model. Evaluating the data, and performance of the model, letting the ML engineer if any issue is happening. 


### MLOps Maturity Model
One of the questions is howe to improve a model. 

there are 5 levels of maturity defined in MLOps from 0 to 5:

    0 - No MLOps: Raw ML no automatic leveling
                  All code in Notebooks.

    1 - DevOps but no MLOps:
                Releases are atutomated, there are integration tests, Unit and integration tests, CI/CD, Ops Metrics. 
                No Experiment tracking
                No reproducibility
                DS Separated from Engineers.

    2 - Automated training:
                Training Pipeline
                Experiment Tracking
                Model Registry
                Low Friction Deployment
                DS work with Engineers. 

    3 - Automated Model Deployment:
                Easy to deploy model
                Data Prep --> Train Model --> Deploy Model
                A/B Testing 
                Model Monitoring.

    4 - Full MLOps automation.:
                Automatic Training and reTraining and deployment. 
                 



