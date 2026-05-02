FROM python:3.10
WORKDIR /
COPY search_patch /search_patch
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/platformio/platformio-core.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /platformio-core/. /repo && rm -rf /platformio-core/
RUN rm -rf /platformio-core
RUN find /repo -name "requirements*.txt" -o -name "Pipfile*" -o -name "pyproject.toml" -o -name "poetry.lock" 2>/dev/null
RUN cd /repo && pip install -e . -q
RUN pip show click | grep Version
RUN pip install twisted==18.9.0
RUN pip install jsondiff==2.2.1
RUN pip install click==8.0.4 -q
RUN pip install pyopenssl==26.0.0
RUN pip install service_identity==24.2.0
RUN pip show twisted | grep Version
RUN pip install twisted==21.7.0 -q
RUN pip install constantly==23.10.4
RUN pip install twisted==18.9.0 -q