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
RUN find /repo -name "requirements*.txt" -o -name "Pipfile*" -o -name "environment.yml" 2>/dev/null
RUN cat /repo/.github/workflows/*.yml 2>/dev/null | head -100
RUN pip install numpy==2.2.6
RUN pip install scipy==1.15.3
RUN pip install matplotlib==3.10.8
RUN pip install pytest==9.0.2
RUN pip install pytest-timeout==2.4.0
RUN pip install ruff==0.15.4
RUN pip install numpydoc==1.10.0
RUN cd /repo && pip install -e . -q