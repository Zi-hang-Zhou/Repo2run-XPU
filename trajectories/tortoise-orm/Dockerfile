FROM python:3.10
WORKDIR /
COPY search_patch /search_patch
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/tortoise/tortoise-orm.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /tortoise-orm/. /repo && rm -rf /tortoise-orm/
RUN rm -rf /tortoise-orm
RUN cd /repo && poetry install
RUN pip install asyncpg==0.31.0
RUN pip install pyodbc==5.3.0
RUN cd /repo && poetry add pyodbc==5.1.0
RUN cd /repo && poetry add asyncpg
RUN cd /repo && poetry install --extras asyncpg
RUN cd /repo && poetry add asyncodbc
RUN cd /repo && apt-get update -qq
RUN cd /repo && apt-get install unixodbc -y -qq
RUN cd /repo && poetry install --extras asyncodbc
RUN cd /repo && poetry install --extras aiomysql
RUN cd /repo && poetry install --extras psycopg