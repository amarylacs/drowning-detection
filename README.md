## Components Needed

**Hardware components:**
1. Raspberry Pi 5 (8GB) + 64GB MicroSD card
2. Raspberry Pi AI Camera
3. OPTIONAL: Fan + Heatsink to reduce heating

**Software components**
1. Install Docker by going through this link: ```https://docs.docker.com/engine/install/debian/```
2. Load with Raspberry Pi OS (NOT UBUNTU!)
3. Optional: Trained Roboflow model and/or Roboflow Workflow

All scripts were tested on a Macbook Air (Tahoe/Sequoia), Google Colab (T4), and VSCode. 

# Installation Instructions for local detection (through VSC + Docker + Roboflow)

This installation will use several Python scripts to execute model inference on one image stored as a file, and does not utilize the RPI AI camera. For live detection with the AI Camera, see [Live Detection on the Raspberry Pi AI Camera](#live-detection-on-the-raspberry-pi-ai-camera).

## Install Pyenv

1. ``` $ git clone https://github.com/pyenv/pyenv.git ~/.pyenv ```

2. ``` $ nano ~/.bashrc ```

3. To the bottom of the file, add:
  ``` export PYENV_ROOT="${HOME}/.pyenv"
  if [ -d "${PYENV_ROOT}" ]; then
      export PATH=${PYENV_ROOT}/bin:$PATH
      eval "$(pyenv init -)"
  fi
  ```

## Install Python 3.12 using Pyenv
*Raspberry Pi's OS automatically sets Python 3.13 as its default version, but Roboflow's inference server can only be installed on Python versions < 3.13*

4. ```$ pyenv install 3.12.7 ```

  4.5. To check if Python 3.12.7 was actually installed, run ``` which python3.12 ```, and ```/home/username/.pyenv/shims/python3.12``` should return.

## Create and activate a Virtual Environment using Python3.12

5. ```$ pyenv virtualenv 3.12 raspi ```

  For clarity, I've named my virtual environment ```raspi```.

6. ```$ pyenv activate raspi```

  You should see ```(raspi) user@user:~ $``` on your bash line.

6.5. Check your Python version to confirm 3.12:

```$ python --version```

## Download Roboflow's packages and start an Inference Server

7. ```$ pip install inference-sdk && pip install roboflow && pip install inference-cli```

8. ```$ inference server start```

This step takes a few minutes! It should say ```Starting inference server container...```
If it DOESN'T, maybe install Docker again!

## Run your code file

9. FORK this rep and fill in the API Keys and necessary models, workflows, etc.

10. ```$ cd``` into your parent folder (example: ```$ cd Documents/GitHub/drowning-detection```

11. ```$ python3 <file_name>``` (example: ```$ python3 default-single-inference.py```

12. To deactivate the environment (to close it, not delete it), ```$ deactivate```

# Live Detection on the Raspberry Pi AI Camera
This portion will run through model training, conversion/quantization onto the IMX500, and scripts to run a custom model on the Raspberry Pi AI Camera. For pre-trained models on Roboflow, testing is currently ongoing. As of now, only a custom trained YOLOv11 model on Google Colab has been completely tested with this pipeline. 

## On your local computer, gather a dataset
For accurate models, around 1,000 - 2,000 images should work well. [Roboflow](https://roboflow.com) is a good website for annotating your dataset. Export as a .zip file.

## Model Training
For training in Google Colab, please use the following scripts after adding your dataset zip file into contents (updated 07/26/2026)

### Install packages

```
!pip install -q ultralytics "imx500-converter[pt]" model-compression-toolkit

import zipfile
import os
from ultralytics import YOLO
# Restart your session afterwards (DO NOT DELETE IT THO)
```
Restart your session afterwards, if needed. You should see all packages install without errors. For warnings about outdated versions of pip or dependencies, ignore (unless future steps result in a catastrophe)

### Upload dataset
```
zip_filename = "/content/your-dataset-name.zip" 
extract_dir = "/content/dataset"

with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

print("Dataset extracted")
```
"Dataset extracted" is a good sign.
### Train Model (skip if you already have weights)
```
model = YOLO("yolo11n.pt")

results = model.train(
    data=f"{extract_dir}/data.yaml", 
    epochs=50, 
    imgsz=640
)
```
This step (training your model) will take a while depending on the size of your dataset. I suggest settling down with a cup of tea and briefly monitoring your mAP score. It should steadily grow over time. WARNING: The IMX500, which is the sensor used in the RPI-AI-CAM, will only take nano versions of YOLOv11 (otherwise known as YOLOv11n). YOLOv11s is a risk, while versions of YOLOv8 remain untested. 


After training, you should see something akin to `50 epochs completed in 0.394 hours` and `Results saved to /content/runs/detect/train` in your Colab output along with a YOLO summary. Do not ignore any warnings or errors that pop up!

#### Case dependent: Install missing dependencies

```
!pip install --upgrade "protobuf>=5.27.0"
# Restart your session afterwards! (DO NOT DELETE YOUR SESSION THO)
```
If you didn't see the comment, restart your session afterwards. Protobuf was a little corrupted in my case. It never hurts to run! If the next step fails, read the error message and figure out if you're missing any packages. 

### Create a mini calibration set
In many cases, the validation set from your dataset will be too large for the Colab T4 and crash the CPU, whoops. In this case, make a mini calibration set of just 40 images. You'll have to adjust the code for other OS systems

```
import os
import shutil
import yaml

mini_dir = "/content/mini_calib"
os.makedirs(f"{mini_dir}/images/val", exist_ok=True)
os.makedirs(f"{mini_dir}/labels/val", exist_ok=True)

val_imgs = [f for f in os.listdir("/content/dataset/valid/images") if f.endswith(('.jpg', '.jpeg', '.png'))][:40] 

# You can change the number of images ^^^^, but >300 is kind of crazy. 

for img in val_imgs:
    shutil.copy(f"/content/dataset/valid/images/{img}", f"{mini_dir}/images/val/{img}")
    lbl = os.path.splitext(img)[0] + ".txt"
    lbl_path = f"/content/dataset/valid/labels/{lbl}"
    if os.path.exists(lbl_path):
        shutil.copy(lbl_path, f"{mini_dir}/labels/val/{lbl}")

with open("/content/dataset/data.yaml", "r") as f:
    orig_yaml = yaml.safe_load(f)

mini_yaml = {
    "path": mini_dir,
    "train": "images/val",
    "val": "images/val",
    "names": orig_yaml.get("names", {0: "object"})
}

with open("/content/mini_data.yaml", "w") as f:
    yaml.dump(mini_yaml, f)

print(f"Created mini dataset with {len(val_imgs)} calibration images.")
```

### Export your model with Model Compression Toolkit

```
from ultralytics import YOLO

model = YOLO('/content/runs/detect/train/weights/best.pt')

model.export(format="imx", data="/content/mini_data.yaml")
```

This step took me (on T4) 17 minutes and will either make or break your model. This is where your model is quantized into INT8 to "fit" onto the RPI AI Camera, and probably where things go wrong the most. In the case of errors either now or in the future, please reference [Troubleshooting](#troubleshooting)

### Send packerOut.zip to your Raspberry Pi
Email, USB drive, etc. Save wherever you deem fit. For my reference, packerOut.zip will be in `~/Downloads`.

### Setting up Pi
(Future steps will now be on the Pi instead of your local computer) Open a terminal:
```
sudo apt update
sudo apt install imx500-all imx500-tools -y
sudo reboot
```

### Convert your model to .rpk Firmware
```
imx500-package -i ~/Downloads/packerOut.zip -o ~/
```
The output should be a file `~/network.rpk`. This is another step where things can start to fall apart. For errors, reference [Troubleshooting](#troubleshooting).

#### Case dependent: Identify your classes
In your Google Colab file, run
```
from ultralytics import YOLO

model = YOLO('/content/runs/detect/train/weights/best.pt')

for idx, name in model.names.items():
    print(f"Index {idx}: {name}")
```
to identify your classes and their order. You'll need this for the next step. In my case, the output was 2 classes: drowning and normal.
```
# JULES'S OUTPUT:
Index 0: drowning
Index 1: normal
```

### Create Post Processing .json file

You can do this via cat on bash. This is an example of what my file looks like, you'd want to change a few paths or values depending on your circumstances.

```
cat << 'EOF' > ~/model_config.json
{
    "imx500_object_detection":
    {
        "max_detections": 10,
        "threshold": 0.3,
        "bbox_normalization": true,
        "bbox_order": "xy",
        "network_file": "/home/pi-name/network.rpk",
        "temporal_filter":
        {
            "tolerance": 0.1,
            "factor": 0.2,
            "visible_frames": 4,
            "hidden_frames": 2
        },
        "classes":
        [
            "drowning",
            "normal"
        ]
    },
    "object_detect_draw_cv":
    {
        "line_thickness": 2,
        "font_scale": 0.6
    }
}
EOF
```

### Creating labels file 

```
cat << 'EOF' > ~/labels.txt
drowning
normal
EOF
```

### Running the Model

```
cd ~/picamera2/examples/imx500
python3 imx500_object_detection_demo.py --model ~/network.rpk --labels ~/labels.txt --threshold 0.3 --bbox-normalization --bbox-order xy
```

# Troubleshooting

## Hardware Components
1. [Raspberry Pi Getting Started](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html)
2. [Raspberry Pi AI Camera Documentation](https://www.raspberrypi.com/documentation/accessories/ai-camera.html)

## IMX500 Quantization, Export, MCT, etc. etc. etc.
1. [Ultralytics Documentation for Sony IMX500 on YOLO11 sample models](https://docs.ultralytics.com/integrations/sony-imx500#using-imx500-export-in-deployment)
2. [Sony Model Compression Tookit Github](https://github.com/SonySemiconductorSolutions/mct-model-optimization)
3. [Raspberry Pi AI Camera IMX500 Converter User Manual](https://developer.aitrios.sony-semicon.com/en/docs/raspberry-pi-ai-camera/imx500-converter)
