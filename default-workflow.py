from inference_sdk import InferenceHTTPClient
import json

client = InferenceHTTPClient(
    api_url="http://localhost:9001", 
    api_key="11vRFtlNLadjkcqsK6FG"
)

result = client.run_workflow(
    workspace_name="roboflow-docs",
    workflow_id="model-comparison",
    images={
        "image": "construction.jpg"
        #"https://media.roboflow.com/workflows/examples/bleachers.jpg"
    },
    parameters={
        "model1": "yolov8n-640",
        "model2": "yolov11n-640"
    }
)


workflow_output = result[0]

if isinstance(workflow_output, dict):

    for key, value in workflow_output.items():
        if key != 'model_comparison_visualization':  # skip the image data
            if isinstance(value, (dict, list)):
                print(f"\n{key}:")
                print(json.dumps(value, indent=2))
            else:
                print(f"{key}: {value}")


print("\nhello")