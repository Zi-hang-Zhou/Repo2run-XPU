FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/piccolo-orm/piccolo.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /piccolo/. /repo && rm -rf /piccolo/
RUN rm -rf /piccolo
RUN pip install black==26.1.0
RUN pip install colorama==0.4.6
RUN pip install jinja2==3.1.6
RUN pip install targ==0.6.0
RUN pip install inflection==0.5.1
RUN pip install typing-extensions==4.15.0
RUN pip install pydantic==2.12.5
RUN pip install coveralls==3.3.1
RUN pip install httpx==0.28.0
RUN pip install pytest-cov==3.0.0
RUN pip install pytest==8.3.5
RUN pip install python-dateutil==2.8.2
RUN pip install asyncpg==0.31.0
RUN pip install aiosqlite==0.22.1
ENV PICCOLO_CONF="tests.sqlite_conf"