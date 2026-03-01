FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/huggingface/datasets.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /datasets/. /repo && rm -rf /datasets/
RUN rm -rf /datasets
RUN find /repo -name "requirements*.txt" -o -name "requirements*.in" 2>/dev/null | head -20
RUN cd /repo && pip install -e . -q
RUN cd /repo && pip install -e .[tests] -q