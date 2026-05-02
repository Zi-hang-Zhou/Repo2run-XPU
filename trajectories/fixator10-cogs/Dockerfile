FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/fixator10/fixator10-cogs.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /fixator10-cogs/. /repo && rm -rf /fixator10-cogs/
RUN rm -rf /fixator10-cogs
RUN ls /repo/*.lock 2>/dev/null || echo "No lock files found"
RUN find /repo -name "test*.py" -o -name "*_test.py" 2>/dev/null | head -20
RUN cat /repo/.github/workflows/*.yml 2>/dev/null