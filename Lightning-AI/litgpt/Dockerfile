FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/Lightning-AI/litgpt.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /litgpt/. /repo && rm -rf /litgpt/
RUN rm -rf /litgpt
RUN find /repo -name "requirements*.txt" -o -name "Pipfile*" -o -name "environment.yml" 2>/dev/null
RUN cd /repo && pip install -e .[test] -q
RUN cd /repo && pip install -e .[extra] -q