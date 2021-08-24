import os
import json
import joblib
import re
import pandas as pd
import datetime

from azureml.core import Workspace, Experiment, Dataset
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core.model import Model
from azureml.core.webservice import Webservice
from azureml.core.run import Run

run = Run.get_context()
#run = Experiment.start_logging()
ws = run.experiment.workspace

if __name__ == "__main__":
    # Loading azure credentials
    # print("::debug::Loading azure credentials")
    # azure_credentials = os.environ.get("INPUT_AZURE_CREDENTIALS", default="{}")

    # # Loading parameters file
    # print("::debug::Loading parameters file")
    # parameters_file = os.environ.get("INPUT_PARAMETERS_FILE", default="workspace.json")
    # parameters_file_path = os.path.join(".cloud", ".azure", parameters_file)
    # try:
    #     with open(parameters_file_path) as f:
    #         parameters = json.load(f)
    # except FileNotFoundError:
    #     print(f"::debug::Could not find parameter file in {parameters_file_path}. Please provide a parameter file in your repository if you do not want to use default settings (e.g. .cloud/.azure/workspace.json).")
    #     parameters = {}

    # if azure_credentials.get("resourceManagerEndpointUrl", "").startswith("https://management.usgovcloudapi.net"):
    #     cloud = "AzureUSGovernment"
    # elif azure_credentials.get("resourceManagerEndpointUrl", "").startswith("https://management.chinacloudapi.cn"):
    #     cloud = "AzureChinaCloud"
    # else:
    #     cloud = "AzureCloud"
    
    # sp_auth = ServicePrincipalAuthentication(
    #     tenant_id=azure_credentials.get("tenantId", ""),
    #     service_principal_id=azure_credentials.get("clientId", ""),
    #     service_principal_password=azure_credentials.get("clientSecret", ""),
    #     cloud=cloud
    # )

    # print("::debug::Loading existing Workspace")
    # # Default workspace and resource group name
    # repository_name = str(os.environ.get("GITHUB_REPOSITORY")).split("/")[-1]

    # ws = Workspace.get(
    #     name=parameters.get("name", repository_name),
    #     subscription_id=azure_credentials.get("subscriptionId", ""),
    #     resource_group=parameters.get("resource_group", repository_name),
    #     auth=sp_auth
    # )

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
    
    # loading endpoint
    # aci_service= Webservice(ws, "diabetes-detection-master")
    # logs = aci_service.get_logs()
    todays_date = datetime.datetime.today().strftime('%d/%b/%Y')
    todays_date = todays_date.replace("/", "-")
    # logs = logs[logs.find(todays_date):]

    # endpoint_inputs = re.findall("{'data': (.*?)}", logs)
    # input_data_list = []
    # for x in endpoint_inputs:
    #     temp = []
    #     for str_input in x[2:-2].split(", "):
    #         temp.append(float(str_input))
    #     input_data_list.append(temp)
        
    # new_df = pd.DataFrame(input_data_list, columns=['Pregnancies','Glucose','BloodPressure','SkinThickness','Insulin','BMI','DiabetesPedigreeFunction','Age'])

    dataset_name = "diabetes-freshdata-" + todays_date
    diabetes_ds = Dataset.get_by_name(ws, dataset_name)
    new_df = diabetes_ds.to_pandas_dataframe()

    array = new_df.values

    x = array[:, 0:8]
    ground_truth = array[:, 8]
    ground_truth = [int(i) for i in ground_truth]

    predicted_output = current_model.predict(x)
    predicted_output = [int(i) for i in predicted_output]

    # print(os.getcwd())

    # ground_truth_path = os.path.join("ground", "result.txt")
    # file1 = open(ground_truth_path, 'r')         # modify path accordingly
    # Lines = file1.readlines()
    # ground_truth = []

    # for line in Lines:
    #     ground_truth.append(int(line.strip()))
    # new_df['Outcome'] = ground_truth
        
    correct = 0
    for i, label in enumerate(ground_truth):
        if ground_truth[i] == predicted_output[i]:
            correct += 1

    accuracy = correct/len(ground_truth)

    #print("pradeep_fresh_data_accuracy", accuracy)
    print("::debug::Creating outputs")

    run.log("pradeep_fresh_data_accuracy", 12)
    #run_metrics_markdown = convert_to_markdown(run_metrics)
    #print(f"::set-output name=run_metrics_markdown::{run_metrics_markdown}")

    #print(f"::set-output name=pradeep_fresh_data_accuracy_2::23")
    #run.log(f"::set-output name=pradeep_fresh_data_accuracy::{accuracy}")
    
    #print(f"::set-output name=pradeep_fresh_data_accuracy::{accuracy}")

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