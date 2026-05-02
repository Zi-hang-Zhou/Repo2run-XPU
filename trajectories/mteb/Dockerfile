FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/embeddings-benchmark/mteb.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /mteb/. /repo && rm -rf /mteb/
RUN rm -rf /mteb
RUN find /repo -name "requirements*.txt" -o -name "poetry.lock" -o -name "Pipfile*" 2>/dev/null
RUN cat /repo/.github/workflows/*.yml 2>/dev/null | head -100
RUN cd /repo && pip install -q .[dev,speedtask]