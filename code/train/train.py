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
from azureml.core import Workspace, Dataset
from azureml.core.run import Run
from azureml.core.model import Model
from azureml.core.experiment import Experiment

run = Run.get_context()
ws = run.experiment.workspace

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     '--data_path',
    #     type=str,
    #     help='Path to the training data'
    # )

    # args = parser.parse_args()
    # print("LIST FILES IN DATA PATH...")
    # data_files = os.listdir(args.data_path)
    # print(data_files)

    # file_path = os.path.join(os.getcwd(), data_files[0])
    # print(file_path)
    # ws = Workspace.from_config()
    # ensure diabetes_ds is already registerd as a dataset

    diabetes_ds = Dataset.get_by_name(ws, 'diabetes_ds')
    df = diabetes_ds.to_pandas_dataframe()

    todays_date = datetime.datetime.today().strftime('%d/%b/%Y')
    todays_date = todays_date.replace("/", "-")

    dataset_name = "diabetes-freshdata-" + todays_date
    #diabetes_ds = Dataset.get_by_name(ws, dataset_name)
    diabetes_ds = Dataset.get_by_name(ws, 'diabetes-freshdata-24-Aug-2021')
    new_df = diabetes_ds.to_pandas_dataframe()
    array = new_df.values
    recent_x = array[:, 0:8]
    recent_y = array[:, 8]

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

    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=7)

    model = LogisticRegression(max_iter=100000)
    # model.fit(x_train, y_train)
    # result = model.score(x_test, y_test)
    model.fit(x, y)
    result = model.score(recent_x, recent_y)

    # print(f"::set-output name=accuracy::{result}")

    # labels = ['Negative', 'Positive']
    # labels_numbers = [0, 1]
    # cm = confusion_matrix(y_test, result, labels_numbers)
    
    # outputs directory is automatically created so dump models here
    modelfile = 'outputs/model.pkl'
    joblib.dump(model, modelfile)

    # accessing previous experiment
    experiment = Experiment(workspace=ws, name='diabetes-detection-monitor-via-aml')
    list_experiments = Experiment.list(ws)
    list_runs = experiment.get_runs()       # generated only once
    i = 0

    for run in list_runs:                   # access last experiment
        if i == 1:
            metrics = run.get_metrics()
            print(run.id)
            break
        i += 1
    
    # metrics = recent_expt.get_metrics()
    prev_accuracy = metrics.get('Fresh_data_accuracy')
    print(prev_accuracy)

    # Changing deployed model tag
    if prev_accuracy < result:
        production_model = ""
        model_version = 1

        for model in Model.list(ws):
            print(model.name, 'version:', model.version)
            if "production" in model.tags.values():
                production_model = model.name
                model_version = model.version
                break
        
        model = Model(ws, production_model, version=model_version)
        model.remove_tags('type')
    
    run.log('Intercept', model.intercept_)
    run.log('Slope', model.coef_[0])
    run.log("Experiment end time", str(datetime.datetime.now()))
    # logging model accuracy on fresh dataset
    run.log("model_accuracy", result)
    
    run.complete()
    
    print("Finished training!!")