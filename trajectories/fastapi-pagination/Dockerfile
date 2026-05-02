FROM python:3.10
WORKDIR /
COPY search_patch /search_patch
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
RUN cd /repo && poetry install
RUN pip install aiosqlite==0.17.0
RUN pip index versions aiosqlite --python-version 3.10
RUN cd /repo && poetry add --group dev "aiosqlite>=0.17.0,<0.20.0"
RUN pip index versions asyncpg --python-version 3.10
RUN cd /repo && poetry add --group dev "asyncpg>=0.24.0,<0.29.0"
RUN cd /repo && poetry install
RUN cd /repo && poetry show pydantic
RUN cd /repo && poetry run python -c "import pydantic; print(pydantic.__version__)"
RUN cd /repo && pip install -e .
RUN cd /repo && pip install pydantic>=1.9.1,<2.0
RUN pip install asyncpg>=0.24.0,<0.29.0
RUN pip install asgi_lifespan>=2.1.0
RUN pip install cassandra-driver>=3.25.0
RUN pip install fastapi>=0.93.0
RUN pip install pydantic>=1.9.1,<2.0 fastapi>=0.93.0,<0.100.0
RUN pip install httpx>=0.27.0
RUN pip install motor>=2.5.1,<4.0.0
RUN pip install pytest-asyncio>=0.21.1
RUN pip install Faker>=25.9.1
RUN pip install pytest-cov>=5.0.0
RUN pip install sqlalchemy>=2.0.0
RUN pip install httpx>=0.23.0,<0.25.0
RUN cd /repo && pip install databases>=0.6.0 beanie>=1.25.0 tortoise-orm>=0.16.18,<0.21.0 mongoengine>=0.23.1,<0.29.0 ormar>=0.11.2 piccolo>=0.89,<0.122 pony>=0.7.16 bunnet>=1.1.0 django>=4.0,<5.0.0
RUN cd /repo && pip install pydantic>=1.9.1,<2.0 fastapi>=0.93.0,<0.100.0
RUN pip uninstall -y beanie mongoengine ormar tortoise-orm bunnet
RUN cd /repo && pip install beanie>=1.25.0,<2.0 tortoise-orm>=0.16.18,<0.20.0 mongoengine>=0.23.1,<0.27.0 bunnet>=1.1.0,<1.2.0
RUN pip uninstall -y beanie mongoengine
RUN pip install pymongo<4.0 beanie>=1.25.0,<2.0
RUN pip install mongoengine>=0.23.1,<0.27.0
RUN pip uninstall -y beanie
RUN cd /repo && pip index versions pytest --python-version 3.10
RUN cd /repo && pip install pytest>=7.0.0,<8.0.0
RUN cd /repo && pip install pytest-asyncio>=0.21.1,<1.0.0
RUN cd /repo && pip install pytest>=7.0.0,<8.0.0 pytest-asyncio>=0.21.1,<0.24.0
RUN pip install pytest-asyncio>=0.21.1,<0.22.0
RUN pip install beanie>=1.25.0,<1.26.0