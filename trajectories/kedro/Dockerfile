FROM python:3.10
WORKDIR /
COPY search_patch /search_patch
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/kedro-org/kedro.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /kedro/. /repo && rm -rf /kedro/
RUN rm -rf /kedro
RUN ls -la /repo/*.lock /repo/*.txt /repo/setup.py 2>/dev/null || echo "No lock or txt files found"
RUN find /repo -name "requirements*.txt" -type f 2>/dev/null
RUN cd /repo && pip install -e .[test] -q