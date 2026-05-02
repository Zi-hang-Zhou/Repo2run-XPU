FROM python:3.10
WORKDIR /
COPY search_patch /search_patch
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/ourresearch/oadoi.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /oadoi/. /repo && rm -rf /oadoi/
RUN rm -rf /oadoi
RUN pip install mock==5.2.0 sendgrid==6.12.5 -q
RUN pip install sqlalchemy==2.0.49 requests_cache==1.3.1 -q
RUN pip install boto3==1.43.1 ddt==1.7.2 -q
RUN pip install flask==3.1.3 nose==1.3.7 -q
RUN pip install flask-compress==1.24 lxml==6.1.0 -q
RUN pip install flask-debugtoolbar==0.16.0 psycopg2-binary==2.9.12 -q
RUN pip install flask-sqlalchemy==3.1.1 -q
ENV OPENALEX_DATABASE_URL="postgresql://user:password@localhost:5432/testdb"
ENV OPENALEX_DATABASE_URL="postgresql://user:password@localhost:5432/testdb"
ENV DATABASE_URL="postgresql://user:password@localhost:5432/testdb"
RUN pip install shortuuid==1.0.13 heroku3==5.2.1 -q
ENV OPENALEX_DATABASE_URL="postgresql://user:password@localhost:5432/testdb"
ENV DATABASE_URL="postgresql://user:password@localhost:5432/testdb"
RUN pip install tenacity==9.1.4 beautifulsoup4==4.14.3 -q
ENV OPENALEX_DATABASE_URL="postgresql://user:password@localhost:5432/testdb"
ENV DATABASE_URL="postgresql://user:password@localhost:5432/testdb"
RUN pip install redis==7.4.0 -q
ENV OPENALEX_DATABASE_URL="postgresql://user:password@localhost:5432/testdb"
ENV DATABASE_URL="postgresql://user:password@localhost:5432/testdb"
RUN pip install unidecode==1.4.0 -q
ENV OPENALEX_DATABASE_URL="postgresql://user:password@localhost:5432/testdb"
ENV DATABASE_URL="postgresql://user:password@localhost:5432/testdb"
RUN ls -la /repo/*.cfg /repo/*.ini /repo/pyproject.toml 2>/dev/null || echo "No config files found"
RUN echo 'import os' > /repo/test/conftest.py
RUN echo 'from app import app, db' >> /repo/test/conftest.py
RUN echo '' >> /repo/test/conftest.py
RUN echo 'os.environ.setdefault("OPENALEX_DATABASE_URL", "postgresql://user:password@localhost:5432/testdb")' >> /repo/test/conftest.py
RUN echo 'os.environ.setdefault("DATABASE_URL", "postgresql://user:password@localhost:5432/testdb")' >> /repo/test/conftest.py
RUN echo '' >> /repo/test/conftest.py
RUN echo 'def app_context():' >> /repo/test/conftest.py
RUN echo '    with app.app_context():' >> /repo/test/conftest.py
RUN echo '        yield' >> /repo/test/conftest.py
RUN echo 'import os' > /tmp/write_conftest.py
RUN echo 'content = """import os' >> /tmp/write_conftest.py
RUN echo 'from app import app, db' >> /tmp/write_conftest.py
RUN echo '' >> /tmp/write_conftest.py
RUN echo 'os.environ.setdefault("OPENALEX_DATABASE_URL", "postgresql://user:password@localhost:5432/testdb")' >> /tmp/write_conftest.py
RUN echo 'os.environ.setdefault("DATABASE_URL", "postgresql://user:password@localhost:5432/testdb")' >> /tmp/write_conftest.py
RUN echo '' >> /tmp/write_conftest.py
RUN echo 'def app_context():' >> /tmp/write_conftest.py
RUN echo '    with app.app_context():' >> /tmp/write_conftest.py
RUN echo '        yield' >> /tmp/write_conftest.py
RUN echo '"""' >> /tmp/write_conftest.py
RUN echo 'open("/repo/test/conftest.py", "w").write(content)' >> /tmp/write_conftest.py
RUN python /tmp/write_conftest.py
ENV OPENALEX_DATABASE_URL="postgresql://user:password@localhost:5432/testdb"
ENV DATABASE_URL="postgresql://user:password@localhost:5432/testdb"
RUN pip install cachetools==7.0.6 -q
ENV OPENALEX_DATABASE_URL="postgresql://user:password@localhost:5432/testdb"
ENV DATABASE_URL="postgresql://user:password@localhost:5432/testdb"
RUN pip install kids.cache==0.0.7 -q
ENV OPENALEX_DATABASE_URL="postgresql://user:password@localhost:5432/testdb"
ENV DATABASE_URL="postgresql://user:password@localhost:5432/testdb"
RUN apt-get update -qq
RUN apt-get install -y -qq libpoppler-cpp-dev
RUN pip install pdftotext==3.0.0 -q
ENV OPENALEX_DATABASE_URL="postgresql://user:password@localhost:5432/testdb"
ENV DATABASE_URL="postgresql://user:password@localhost:5432/testdb"
RUN pip install sickle==0.7.0 -q
ENV OPENALEX_DATABASE_URL="postgresql://user:password@localhost:5432/testdb"
ENV DATABASE_URL="postgresql://user:password@localhost:5432/testdb"