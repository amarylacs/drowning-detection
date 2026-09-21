# Project Overview
This project is a drowning detection device for residential pools and consists of over 500+ augmented images of adult and infant drowning. This data was then used to train a YOLOv11n model and applied to a Raspberry Pi 5 8GB paired with a Raspberry Pi AI Camera for live inference. This repository holds scripts for local inference on the Pi SoC and real-time inference on the Raspberry Pi AI camera.

The project goal is to make a device that will recognize a variety of swimming and drowning, including treading water, swimming strokes, active drowning, and passive drowning. By using image-to-image diffusion pipelines to augment data and introduce infant drowning varities, this YOLOv11n model reached an mAP score of 92.8% when trained on Roboflow. 

# Repository Layout
```
.
|-- README.md                               #Project introduction
|-- CONTRIBUTING.md                         #Setup for local/real-time inference
|-- LICENSE                                 #Project license
|-- local_inference
|   |-- assets                              #Sample images
|   |-- custom-single-inference.py          #Inference of one photo on a custom model
|   |-- custom-workflow.py                  #Workflow inference on a custom model
|   |-- default-single-inference.py         #Inference of one photo on a default model
|   |-- default-workflow.py                 #Workflow inference on a default model
|   `-- installation.sh                     #Pyenv installation and setup
`-- rpi_cam
    |-- 09-20-26model_config.json           #Sample .json config file
    |-- 09-20-26network.rpk                 #Sample network.rpk file
    |-- 09-20-26packerOut.zip               #Sample packerOut.zip file
    |-- imx500_model_conversion.ipynb       #Google Colab tutorial for model conversion
    |-- labels.txt                          #Sample labels.txt file
    `-- rpi_cam.sh                          #Shell script to run RPI AI Camera

4 directories, 14 files
```

# Documentation
- [CONTRIBUTING.md](/CONTRIBUTING.md): setup for local and real-time inference
- [LICENSE.md](/LICENSE): project license