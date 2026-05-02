FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/dtmilano/androidviewclient.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /androidviewclient/. /repo && rm -rf /androidviewclient/
RUN rm -rf /androidviewclient
RUN find /repo -name "requirements*.txt" -o -name "pyproject.toml" -o -name "poetry.lock" 2>/dev/null
RUN cat /repo/.github/workflows/*.yml 2>/dev/null || cat /repo/.github/workflows/*.yaml 2>/dev/null
RUN cd /repo && pip install -e . -q