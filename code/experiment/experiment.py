import joblib
import datetime
from sklearn.ensemble import RandomForestClassifier

from azureml.core import Workspace, Experiment, Dataset
from azureml.core.model import Model
from azureml.core.run import Run

## --- Experiment Parameters ----##
max_depth = 5
n_estimators = 5
## ------------------------------##
run = Run.get_context()
ws = run.experiment.workspace

if __name__ == "__main__":

    # Loading registered model
    # production_model = ""

    # for model in Model.list(ws):
    #     print(model.name, 'version:', model.version)
    #     if "production" in model.tags.values():
    #         production_model = model.name
    #         break
    
    # model_path = Model.get_model_path(production_model, _workspace=ws)
    # current_model = joblib.load(model_path)
    experiment_model = RandomForestClassifier(n_estimators = n_estimators,max_depth = max_depth)

    todays_date = datetime.datetime.today().strftime('%d/%b/%Y')
    todays_date = todays_date.replace("/", "-")
    fresh_ds = "diabetes_ds"

    fresh_diabetes_ds = Dataset.get_by_name(ws, fresh_ds)
    new_df = fresh_diabetes_ds.to_pandas_dataframe()
    print(new_df.drop(columns='Outcome'))
    array = new_df.values
    x = new_df.drop(columns='Outcome')
    # scaler = MinMaxScaler(feature_range =(0,1))
    # rescaledx = scaler.fit_transform(x)

    # ground_truth = array[:, 8]
    # ground_truth = [int(i) for i in ground_truth]
    ground_truth = new_df['Outcome']
    # predicted_label = current_model.predict(x)
    # predicted_label = [int(i) for i in predicted_label]
        
    # correct = 0
    # for i, label in enumerate(ground_truth):
    #     if ground_truth[i] == predicted_label[i]:
    #         correct += 1

    # current_model_accuracy = current_model.score(x,ground_truth)
    experiment_model.fit(x,ground_truth)
    experiment_accuracy = experiment_model.score(x,ground_truth)
    modelfile = 'outputs/model.pkl'
    joblib.dump(experiment_model, modelfile)
    # print("current_model_accuracy", current_model_accuracy)
    # run.log("current_model_accuracy", current_model_accuracy)
    run.log('New Experiment accuracy',experiment_accuracy)
    # run.log_file()
