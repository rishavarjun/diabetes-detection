import joblib
import datetime
# from sklearn.preprocessing import MinMaxScaler

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
    fresh_ds = "diabetes-ds"

    fresh_diabetes_ds = Dataset.get_by_name(ws, fresh_ds)
    new_df = fresh_diabetes_ds.to_pandas_dataframe()
    
    array = new_df.values
    x = array[:, 0:8]
    # scaler = MinMaxScaler(feature_range =(0,1))
    # rescaledx = scaler.fit_transform(x)

    ground_truth = array[:, 8]
    ground_truth = [int(i) for i in ground_truth]

    predicted_label = current_model.predict(x)
    predicted_label = [int(i) for i in predicted_label]
        
    correct = 0
    for i, label in enumerate(ground_truth):
        if ground_truth[i] == predicted_label[i]:
            correct += 1

    accuracy = correct/len(ground_truth)

    print("Fresh_data_accuracy", accuracy)
    run.log("Fresh_data_accuracy", accuracy)
