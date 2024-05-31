### Module 02: Experiment Tracking

#### Important concepts
ML experiments: The process of building an ML model, the experiment encompasses the whole ML cycle , from playing with models and hyperparameters. 
Artifacts are the files associated with the run and the metadata is the information coming from the model.

#### What is experiment tracking.
It is the process of keeping track of all the *relevant information* from an ML model. A good ML engineer will need to be able to try different versions of the data, test the source,
quality and which information can be included/excluded in the final model. 

    * Source Code
    * Environments
    * Data
    * Model
    * Hyperparameters
    * Metrics

- Why tracking is important? 
    * Rerproducibility
    * Organization
    * Optimization 

Lets imagine the experiment tracking in spreadsheets, the main issues are the how error prone they are, it is not possible to list chnges in the data or model. But also there is not an standard format, and lack of visibility and collaboration since it will be difficult to follow which data was used, which hyperparams were used and so on. 

### MLflow
- Definition: An open source platform for the ML lifecycle.

In practice, it's just a Python package that can be installed with PIP, and contains 4 modules: 

    * Tracking
    * Models
    * Model Registry
    * Projects

MLflow will also automatically logs extra information about the run such as: 
    * Source code
    * Version of the code (git)
    * Start and end time
    * Author

certain variables will be used as parameteres, such as the path to data, metrics and metadata. 

#### Demo
to install Mlflow run first:
- pip install --upgrade setuptools

By launching mlflowui will open a localhost connection where a new experiment can be created. Alognside the experiment mlflow will ask for an artifact location, those can be files, pickle or bento, data. This can be a local folder or an S3 bucket. 

The second tab is for the models, for this a backend register is needed, or database (postgres, mysql, etc)

- The following command will solve that issue:

    mlflow ui --backend-store-uri sqlite:///mlflow.db 

MLflow will allow to compare the result of several runs by comparing the resutls and scores. However, mlflow will allow you to keep track of different parameters for finetuning using:

HyperOpt and XGboost. 

#### 2.4 Model management
When talking about ML lifecycle we are talking about the steps needed to build and maintain a ML model. 

Example Experiment tracking is just a small subset of the MLOps architecture but model management takes also in consideration the model versioning, deployment, and scaling. 

We can use MLflow to track the experiments, hyperparam and tuning, once is finished the next step is to deploy the best model possible and version after. If the model needs to be updated once the scaling happens so the versioning will also be updated. 

Once the model is deployed the prediction monitoring starts.

We can log models with mlflow as artifact or log_model
    - mlflow.log_artifact("my_model", artifact_path="models/")

    - mlflow.<framework>.log_model(model, artifact_path="models/")

#### 2.5 Model registry
If for example, a new model is created.
it is necessary to know what changes are made into the model, in order to push into production. 

MLflow will set a tracking server to keep the model and register the versioning and changes made. 

ML_flow(tracking server) --> MLFlow(Model registry)
model 1, 2                      Staging (v3, v4)
                                Production (V2)
                                archive (v1)

important things to note when comparing models in MLflow
 * Time
 * Lowest Error
 * Size

To register the model, artifacts are needed. There will be the option to register and save into models. 

#### 2.6 MLflow in practice

##### Different scenarios for running MLflow.
    * A single data scientist in ML competition -> In this case having a remote tracking server is an overkill. Since there is no need to track information remotely and there is no need to share with other people. 

    Using the model registry is also not needed since the model will not be deployed to production.  

    * A cross-functional team with one data scientist working on an ML model.

    * Multiple Data Scientist working on multiple ML models -> Here sharing the model and inrformation is a must, other DS can update or tune hyperparams so manage the model registry is important to keep the ML lifecycle. 

Depending on the context, MLflow needs to configured:

1. Backend Store --> Here is where all the metadata is stored.
    - Local Filesystem
    - SQLAlchemy compatible DB (e.g., SQLite)

2. Artifacts Store
    - Local Filesystem
    - remote (e.g., s3 Bucket)

3. Tracking Server
    - No tracking
    - localhost
    - Remote





