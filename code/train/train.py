import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import joblib
import datetime
from azureml.core import Workspace, Dataset
from azureml.core.run import Run
from azureml.core.model import Model
from azureml.core.experiment import Experiment

max_depth=2
n_estimators = 20

run = Run.get_context()
ws = run.experiment.workspace

if __name__ == "__main__":
    # Loading trainining dataset
    diabetes_ds = Dataset.get_by_name(ws, 'iabetes-dataset')
    df = diabetes_ds.to_pandas_dataframe()

    todays_date = datetime.datetime.today().strftime('%d/%b/%Y')
    todays_date = todays_date.replace("/", "-")
    fresh_ds = "new-diabetes-dataset"
    fresh_diabetes_ds = Dataset.get_by_name(ws, fresh_ds)

    new_df = fresh_diabetes_ds.to_pandas_dataframe()
    array = new_df.values
    recent_x = array[:, 0:8]
    recent_y = array[:, 8]

    # instead of printing as a standard out, divert them into azure logs
    run.log("Experiment start time", str(datetime.datetime.now()))

    array = df.values
    x = array[:, 0:8]
    y = array[:, 8]
    # scaler = MinMaxScaler(feature_range =(0,1))
    # rescaledx = scaler.fit_transform(x)

    # model = LogisticRegression(max_iter=100000)
    model = RandomForestClassifier(n_estimators = n_estimators,max_depth = max_depth)
    model.fit(x, y)
    result = model.score(recent_x, recent_y)
    
    # outputs directory is automatically created for every experiment in AML
    modelfile = 'outputs/model.pkl'
    joblib.dump(model, modelfile)

    # accessing the previous experiment. Specify correct experiment name
    experiment = Experiment(workspace=ws, name='diabetes-detection-arjunr-master')
    list_experiments = Experiment.list(ws)
    list_runs = experiment.get_runs()       # generated only once
    i = 0

    for expt_run in list_runs:
        # print(expt_run._run_id)
        if i == 1:
            metrics = expt_run.get_metrics()
            print(expt_run.id)
            break
        i += 1
    
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
    
    # run.log('Intercept', model.intercept_)
    # run.log('Slope', model.coef_[0])
    run.log('max_depth',max_depth)
    run.log('n_estimators',n_estimators)
    run.log("Experiment end time", str(datetime.datetime.now()))
    # logging newly trained model accuracy on the fresh dataset
    run.log("model_accuracy", result)
    run.complete()
    
    print("Finished training!!")