FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/guardrails-ai/guardrails.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /guardrails/. /repo && rm -rf /guardrails/
RUN rm -rf /guardrails
RUN cd /repo && poetry install
RUN cd /repo && poetry env info
RUN cd /repo && poetry run pip list
RUN cd /repo && poetry install --extras dev