from inference_sdk import InferenceHTTPClient
import json

client = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key=""
)


result = client.infer(
    inference_input="pictures/kiddrowning.jpg",
    model_id="small-dataset-ddepb/3"
)

print("DROWNING DETECTION RESULTS")
print("="*50)

if result and 'predictions' in result:
    predictions = result['predictions']
    
    if len(predictions) > 0:
        for i, pred in enumerate(predictions):
            class_name = pred.get('class', 'unknown')
            confidence = pred.get('confidence', 0)
            print(f"\nDetection {i+1}:")
            print(f"  Class: {class_name}")
            print(f"  Confidence: {confidence:.1%}")
            print(f"  Location: x={pred.get('x', 0):.1f}, y={pred.get('y', 0):.1f}")
            print(f"  Size: {pred.get('width', 0):.1f} x {pred.get('height', 0):.1f}")
        
        print(f"\n>>> DROWNING DETECTED with {predictions[0]['confidence']:.1%} confidence")
    else:
        print("\nNo drowning detected in the image")
else:
    print("No predictions returned")