FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/materialsproject/custodian.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /custodian/. /repo && rm -rf /custodian/
RUN rm -rf /custodian
RUN ls -la /repo/*.lock /repo/requirements*.txt 2>/dev/null; find /repo -name "requirements*.txt" -o -name "*.lock" 2>/dev/null | head -20
RUN cat /repo/.github/workflows/*.yml 2>/dev/null || cat /repo/.github/workflows/*.yaml 2>/dev/null
RUN cd /repo && pip install -e .[dev] -q