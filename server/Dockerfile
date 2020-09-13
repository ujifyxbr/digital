FROM nvidia/cuda:10.2-cudnn7-devel

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3.8 python3.8-dev python3.8-tk python3-pip
RUN apt-get install -y cmake git tmux htop tree libsm6 libxext6 libxrender-dev

RUN python3.8 -m pip install --upgrade pip

WORKDIR /app

RUN pip3 install numpy opencv-python==4.3.0.36 Pillow
RUN pip3 install torch==1.5.0+cu101 torchvision==0.6.0+cu101 -f https://download.pytorch.org/whl/torch_stable.html

RUN pip3 install imagecodecs requests
RUN pip3 install cmake dlib

RUN pip3 install facenet-pytorch

RUN pip3 install cython
RUN pip3 install -U 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'
RUN pip3 install 'git+https://github.com/facebookresearch/fvcore'

ENV FORCE_CUDA="1"
ARG TORCH_CUDA_ARCH_LIST="Kepler;Kepler+Tesla;Maxwell;Maxwell+Tegra;Pascal;Volta;Turing"
ENV TORCH_CUDA_ARCH_LIST="${TORCH_CUDA_ARCH_LIST}"

RUN pip3 install 'git+https://github.com/facebookresearch/detectron2.git'
RUN pip3 install face_recognition

RUN pip3 install Flask flask flask-admin flask-login flask-security sqlalchemy email-validator psycopg2-binary python-dotenv

COPY . /app
RUN mkdir -p /app/learning
RUN mkdir -p /app/monitoring

EXPOSE 5000
CMD python3.8 server.py
