from inference_sdk import InferenceHTTPClient
import json

## GO TO ROBOFLOW WEBSITE AND CHANGE WORKFLOW TO LOCAL SERVER!!!!!

client = InferenceHTTPClient(
    api_url="http://localhost:9001",  # changed from cloud to local
    api_key=""
)

result = client.run_workflow(
    workspace_name="science-research-ys1ki",
    workflow_id="detect-count-and-visualize",
    images={"image": "kiddrowning.jpg"},
    parameters={}
)

print(json.dumps(result, indent=2))