FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/alteryx/featuretools.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /featuretools/. /repo && rm -rf /featuretools/
RUN rm -rf /featuretools
RUN find /repo -name "poetry.lock" -o -name "requirements*.txt" 2>/dev/null | head -20
RUN cat /repo/.github/workflows/*.yml 2>/dev/null | head -100
RUN cd /repo && pip install -e .[test,dask] -q