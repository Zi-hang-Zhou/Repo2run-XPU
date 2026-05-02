FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/python-control/python-control.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /python-control/. /repo && rm -rf /python-control/
RUN rm -rf /python-control
RUN find /repo -name "requirements*.txt" -o -name "Pipfile*" -o -name "poetry.lock" 2>/dev/null
RUN cd /repo && pip install -e . -q