import joblib
import datetime

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from azureml.core import Workspace, Experiment, Dataset
from azureml.core.model import Model
from azureml.core.run import Run

## --- Experiment Parameters ----##
max_depth = 20
n_estimators = 20
## ------------------------------##
run = Run.get_context()
ws = run.experiment.workspace

if __name__ == "__main__":

    # todays_date = datetime.datetime.today().strftime('%d/%b/%Y')
    # todays_date = todays_date.replace("/", "-")
    fresh_ds = "diabetes-dataset"

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

    experiment_model = RandomForestClassifier(n_estimators = n_estimators,max_depth = max_depth)
    experiment_model.fit(x_train, y_train)
    accuracy = experiment_model.score(x_test, y_test)
   
    modelfile = 'outputs/model.pkl'
    joblib.dump(experiment_model, modelfile)
    
    experiment_end_time = datetime.datetime.now()
    experiment_duration = (experiment_end_time - experiment_start_time).total_seconds()
    
    run.log('max_depth',max_depth )
    run.log('n_estimators', n_estimators)
    run.log("Experiment duration (s)", str(experiment_duration))
    run.log('Experiment Model accuracy',accuracy)
    run.complete()
    
    print("Finished training!!")