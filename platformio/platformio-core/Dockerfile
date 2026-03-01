FROM python:3.10
WORKDIR /
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
RUN find /repo -name "requirements*.txt" -o -name "pyproject.toml" -o -name "poetry.lock" 2>/dev/null
RUN cd /repo && pip install -e . -q
RUN pip install twisted==25.5.0
RUN pip install jsondiff==2.2.1
RUN pip install pyopenssl==25.3.0
RUN pip install service_identity==24.2.0