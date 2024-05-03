FROM nvcr.io/nvidia/tensorrt:22.04-py3
WORKDIR /opt/work/
ADD requirements.txt /opt/work/
ADD postprocess.py /opt/work/
ADD predict.py /opt/work/
ADD preprocess.py /opt/work/
ADD ts_predictor.py /opt/work/
RUN apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install --quiet -y software-properties-common python3-pip libsm6 libxext6 vim lsof && echo 'export LC_ALL="C.UTF-8"' >> /etc/bash.bashrc && ln -fs /usr/share/zoneinfo/Asia/Taipei /etc/localtime && /usr/bin/python -m pip install --upgrade pip && pip3 install -r requirements.txt
