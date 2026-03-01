FROM python:3.10
WORKDIR /
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
RUN cd /repo && pip install -e . -q
RUN pip install pydantic==2.12.5
RUN pip install asyncpg==0.31.0
RUN pip install psycopg==3.3.3
RUN pip install fastapi==0.133.1
RUN pip install pyodbc==5.3.0
RUN pip install psycopg_pool==3.3.0
RUN pip install asyncodbc==0.1.1
RUN apt-get update -qq
RUN apt-get install unixodbc -y -qq
RUN pip install aiomysql==0.3.2