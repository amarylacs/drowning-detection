# Installation Instructions

## Before Starting...

**Hardware components:**
1. Raspberry Pi 5 (8GB)
2. Raspberry Pi AI Camera

**Software components**
1. Raspberry Pi OS (NOT UBUNTU!)
2. Optional: Trained Roboflow model and/or Roboflow Workflow

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

