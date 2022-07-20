import joblib
import datetime
# from sklearn.ensemble import RandomForestClassifier

from azureml.core import Workspace, Experiment, Dataset
from azureml.core.model import Model
from azureml.core.run import Run


run = Run.get_context()
ws = run.experiment.workspace

if __name__ == "__main__":

    # Loading registered model
    production_model = ""

    for model in Model.list(ws):
        print(model.name, 'version:', model.version)
        if "production" in model.tags.values():
            production_model = model.name
            break
    
    model_path = Model.get_model_path(production_model, _workspace=ws)
    current_model = joblib.load(model_path)
    
    todays_date = datetime.datetime.today().strftime('%d/%b/%Y')
    todays_date = todays_date.replace("/", "-")
    fresh_ds = "diabetes_dataset"

    fresh_diabetes_ds = Dataset.get_by_name(ws, fresh_ds)
    df = fresh_diabetes_ds.to_pandas_dataframe()

    experiment_start_time = datetime.datetime.now()
    
    x = df.drop(columns='Outcome')
    y = df['Outcome']

    scaler = MinMaxScaler(feature_range =(0,1))
    rescaledx = scaler.fit_transform(x)

    test_size = 0.33
    seed = 7

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=seed)

    current_model.fit(x_train, y_train)
    current_model_accuracy = current_model.score(x_test, y_test)
   
    modelfile = 'outputs/model.pkl'
    joblib.dump(current_model, modelfile)
    
    experiment_end_time = datetime.datetime.now()
    experiment_duration = (experiment_end_time - experiment_start_time).total_seconds()
    
    
    run.log("Experiment duration (s)", str(experiment_duration))
    run.log("current_model_accuracy", current_model_accuracy)
    run.complete()
    
    print("current_model_accuracy", current_model_accuracy)
    print("Finished Scoring!!")

