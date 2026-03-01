FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/uriyyo/fastapi-pagination.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /fastapi-pagination/. /repo && rm -rf /fastapi-pagination/
RUN rm -rf /fastapi-pagination
RUN cd /repo && pip install -e .
RUN pip install aiosqlite==0.22.1
RUN pip install asyncpg==0.31.0
RUN pip install pytest==9.0.2
RUN pip install asgi-lifespan==2.1.0
RUN pip install httpx==0.28.1
RUN pip install pytest-asyncio==1.3.0
RUN pip install motor==3.7.1
RUN pip install cassandra-driver==3.29.3
RUN pip install google-cloud-firestore==2.23.0
RUN pip install faker==40.5.1
RUN pip install sqlalchemy==2.0.47
RUN pip install dirty-equals==0.11