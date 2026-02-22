# after downloading Docker...

git clone https://github.com/pyenv/pyenv.git ~/.pyenv
nano ~/.bashrc

#add text
#if [ -d "${PYENV_ROOT}" ]; then
#    export PATH=${PYENV_ROOT}/bin:$PATH
#    eval "$(pyenv init -)"
#fi

pyenv install 3.12.7 

pyenv virtualenv 3.12 raspi 

pyenv activate raspi

python --version

pip install inference-sdk && pip install roboflow && pip install inference-cli

inference server start

cd Documents/GitHub/drowning-detection

python3 default-single-inference.py

deactivate
