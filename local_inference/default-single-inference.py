from roboflow import Roboflow


rf = Roboflow(api_key="")
project = rf.workspace("roboflow-universe-projects").project("construction-site-safety")
model = project.version(25, local="http://localhost:9001/").model


prediction = model.predict(
    "assets/construction.jpg",
    confidence=40,
    overlap = 30)


print(prediction.json())