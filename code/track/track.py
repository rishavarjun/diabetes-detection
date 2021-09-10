import os
import json
import joblib
import re
import pandas as pd
import datetime

from azureml.core import Workspace, Experiment, Dataset
from azureml.core.model import Model
from azureml.core.run import Run

run = Run.get_context()
ws = run.experiment.workspace

if __name__ == "__main__":

    # Loading registered model
    production_model = ""
    # prod_flag = 0

    for model in Model.list(ws):
        print(model.name, 'version:', model.version)
        if "production" in model.tags.values():
            production_model = model.name
            break
    
    model_path = Model.get_model_path(production_model, _workspace=ws)
    # print(model_path)
    current_model = joblib.load(model_path)

    todays_date = datetime.datetime.today().strftime('%d/%b/%Y')
    todays_date = todays_date.replace("/", "-")

    dataset_name = "diabetes_ds"
    diabetes_ds = Dataset.get_by_name(ws, dataset_name)
    new_df = diabetes_ds.to_pandas_dataframe()
    # new_df = new_df.fillna(0)
    array = new_df.values
    # print(array)
    x = array[:, 0:8]
    # print(x)
    ground_truth = array[:, 8]
    ground_truth = [int(i) for i in ground_truth]

    predicted_output = current_model.predict(x)
    predicted_output = [int(i) for i in predicted_output]
        
    correct = 0
    for i, label in enumerate(ground_truth):
        if ground_truth[i] == predicted_output[i]:
            correct += 1

    accuracy = correct/len(ground_truth)

    print("Fresh_data_accuracy", accuracy)
    run.log("Fresh_data_accuracy", accuracy)

    # if accuracy < 0.8:
    #     # updating dataset with ground truth value
    #     diabetes_ds = Dataset.get_by_name(ws, 'diabetes_ds')
    #     main_df = diabetes_ds.to_pandas_dataframe()

    #     frames = [main_df, new_df]
    #     result_df = pd.concat(frames, ignore_index=True)

    #     diabetes_dataset = Dataset.from_pandas_dataframe(result_df, path=None, in_memory=False)
    #     datastore = ws.get_default_datastore()
    #     # Saving file locally and then uploading to datastore and creating modified dataset from it
    #     # May have to use AWS S3 storage here
    #     ds = Dataset.Tabular.register_pandas_dataframe(result_df, datastore, 'diabetes_ds', description = 'diabetes data set')
    #     # now trigger training actions