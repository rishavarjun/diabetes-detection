# from pandas import read_csv
import numpy as np
# from numpy import set_printoptions
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib
import datetime
from sklearn.metrics import confusion_matrix
import os
from azureml.core import Workspace, Experiment, Dataset
from azureml.core.run import Run
run = Run.get_context()
ws = run.experiment.workspace

if __name__ == "__main__":

    diabetes_ds = Dataset.get_by_name(ws, 'diabetes_ds')
    df = diabetes_ds.to_pandas_dataframe()

    # run = exp.start_logging()
    # instead of printing as a standard out, divert them into azure logs
    run.log("Experiment start time", str(datetime.datetime.now()))

    # df = read_csv(file_path)
    array = df.values

    x = array[:, 0:8]
    y = array[:, 8]

    scaler = MinMaxScaler(feature_range =(0,1))
    rescaledx = scaler.fit_transform(x)

    test_size = 0.33
    seed = 7

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=7)

    model = LogisticRegression(max_iter=100000)
    model.fit(x_train, y_train)
    result = model.score(x_test, y_test)
    # run.log("Model result:", result)
    
    # outputs directory is automatically created so dump models here
    modelfile = 'outputs/model.pkl'
    joblib.dump(model, modelfile)
    
    run.log('Intercept:', model.intercept_)
    run.log('Slope:', model.coef_[0])
    run.log("Experiment end time", str(datetime.datetime.now()))
    run.log("Model result:", result)
    run.complete()
    
    print("Finished training!!")