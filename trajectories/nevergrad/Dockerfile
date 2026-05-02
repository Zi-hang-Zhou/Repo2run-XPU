FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/facebookresearch/nevergrad.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /nevergrad/. /repo && rm -rf /nevergrad/
RUN rm -rf /nevergrad
RUN pip install numpy==2.2.6
RUN pip install cma==4.4.4
RUN pip install bayesian-optimization==1.2.0
RUN pip install typing_extensions==4.15.0
RUN pip install pandas==2.3.3
RUN pip install black==24.3.0
RUN pip install mypy==1.20.0
RUN pip install pytest==9.0.3
RUN pip install pytest-cov==7.1.0
RUN pip install pylint==4.0.5
RUN pip install wheel==0.45.1
RUN pip install setuptools==79.0.1
RUN pip show bayesian-optimization
RUN pip index versions bayesian-optimization --python-version 3.10
RUN pip install -q bayesian-optimization==1.2.0
RUN pip install pyomo==5.7.1
RUN pip install gym==0.24.1
RUN pip install pyproj==3.7.1
RUN pip install matplotlib==3.10.8
RUN pip install hyperopt==0.2.7
RUN pip install requests==2.33.1
RUN pip install opencv-python==4.13.0.92
RUN pip install cdt==0.6.0
RUN pip install torch==2.11.0
RUN apt-get update -qq
RUN apt-get install -y -qq libgl1 libglib2.0-0
RUN pip install torchvision==0.26.0