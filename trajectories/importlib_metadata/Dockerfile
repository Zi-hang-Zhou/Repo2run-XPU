FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/python/importlib_metadata.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /importlib_metadata/. /repo && rm -rf /importlib_metadata/
RUN rm -rf /importlib_metadata
RUN find /repo -name "requirements*.txt" -o -name "Pipfile*" -o -name "poetry.lock" 2>/dev/null
RUN cat /repo/.github/workflows/*.yml 2>/dev/null | head -100
RUN cd /repo && pip install -e .[test] -q
RUN apt-get update -qq
RUN apt-get install python3-testresources -y -qq
RUN python --version
RUN pip install testresources==2.0.2 -q 2>&1 || pip==23.0.1 search test 2>&1 | head -20
RUN apt-get install python3.10-full -y -qq 2>&1 | tail -20 || apt-cache search python3.10 | head -20
RUN python -c "import sys; print(sys.version)"
RUN pip install pytest==9.0.3 --upgrade -q
RUN cd /tmp && git clone --depth 1 --branch v3.10.20 https://github.com/python/cpython.git cpython_test 2>&1 | tail -5
RUN cd /tmp && cp -r /tmp/cpython_test/Lib/test /usr/local/lib/python3.10/