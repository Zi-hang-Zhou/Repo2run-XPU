FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/nixtla/neuralforecast.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /neuralforecast/. /repo && rm -rf /neuralforecast/
RUN rm -rf /neuralforecast
RUN cd /repo && pip install -e . -q
RUN pip install scipy==1.15.3
RUN pip install pytest-cov==7.0.0
RUN pip install gitpython==3.1.46
RUN pip install matplotlib==3.10.8
RUN pip install polars==1.38.1
RUN pip install s3fs==2026.2.0