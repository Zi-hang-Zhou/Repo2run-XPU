FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/hips/autograd.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /autograd/. /repo && rm -rf /autograd/
RUN rm -rf /autograd
RUN cd /repo && pip install -e . -q
RUN cd /repo && pip install pytest==9.0.2 pytest-cov==7.0.0 pytest-xdist==3.8.0 -q