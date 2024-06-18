## Model Deployment

From design where we discuss if ML is the right solution for our problem, to train where we set the experiment goal and parameters and create the model itsel. All that is part o the training pipeline, where the result will be a final model. 

In this module we discuss the Operational phase, where we take the inal model and deploy it. 

One important question is the latency or delay in the responses, do we need a prediction now or in a few hours, or weeks (batch deployment or offline deployment). 

- DEployment: 
    - Batch or offline deployment: Runs regularly
    - Online Deployment: UP and Running all the time.
        
        - Webservice: Via HTTP requests
        - Streaming: By a series of events. 


1. Batch Mode: 
    
    Runs the model regularly (Hourly, Daily, MOnthly) regular intervals. By having a database with the data available, and a scoring job that has the model, pulls some data from the database and apply the model to the data. 

    Finally the predictions are pulled into a new database to be reported. 

    - Used for marketing examples, like in the taxi data the user could be deciding in between 2 services taxi or ubers, the model could for example use the predictions to a marketing job helping to improve the platform. 

2. Web Service: 

    The service encompases a specific service. 

    User -> Backend <=> Ride Duration Service (model) 
    
    The user needs to know the duration of the service immediately to choose if to go by taxi or not (price, duration, ...).

3. Streaming: 

    We have producers and consumers, the ocnsumers will feed from the events and do something with the request. 
-
                            -> C1
        Producer -> EVENTS  -> C2
                            -> C3

    There can be segeral producers.

    For example the back end can be the producer, and the event the ride starting. The consumers can be tip prediction, duration of the trip and so on. 

    Similarly, another producer can be duration prediction to improve the performance. 

### Deploying as webservice.

* Create a virtual environment using pipenv
* Creating a script for predictions.
* Putting the script into a flask app.
* Packaging the app to docker.

```bash
docker build -t ride-duration-prediction-service:v1 .
```

```bash
docker run -it --rm -p 9696:9696 ride-duration-prediction-service:v1
```
 Important: It is necessary to find the same exact version used when creating the pickle file. 

 ```bash
 pip freeze | grep scikit-learn
```

Then in the new environemnt (deactivating the previous one) intall the scikit-learn and flask the python version is also needed using pipenv

After loaded the environment weith the versions. It is necessary to create as new py file with the pickle command to open. 





