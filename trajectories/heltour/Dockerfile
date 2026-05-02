FROM python:3.10
WORKDIR /
COPY search_patch /search_patch
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/lichess4545/heltour.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /heltour/. /repo && rm -rf /heltour/
RUN rm -rf /heltour
RUN cd /repo && poetry install
RUN cd /repo && poetry env info
RUN cd /repo && poetry run pip list | grep -i celery
RUN cd /repo && poetry run pip list
RUN cd /repo && poetry run pip install pytest
RUN ls -la /repo/*.ini /repo/*.cfg 2>/dev/null || echo "No ini or cfg files found"
RUN echo -e "import os\nimport django\n\nos.environ.setdefault('DJANGO_SETTINGS_MODULE', 'heltour.settings_testing')\ndjango.setup()" > /repo/conftest.py
RUN echo -e "from .settings_default import *\nCACHEOPS = {\n    '*.*': {'ops': None},\n}\nSTATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'" > /repo/heltour/settings_testing.py
RUN echo -e "from .settings_default import *\nCACHEOPS = {\n    '*.*': {'ops': set()},\n}\nSTATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'" > /repo/heltour/settings_testing.py
RUN echo -e "from .settings_default import *\nCACHEOPS_ENABLED = False\nCACHEOPS = {}\nSTATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'" > /repo/heltour/settings_testing.py
RUN cd /repo && poetry run python -c "f=open('heltour/settings_testing.py','w'); f.write('from .settings_default import *\nCACHEOPS = {\n    \"*.*\": {\"ops\": set()},\n}\nSTATICFILES_STORAGE = \"django.contrib.staticfiles.storage.StaticFilesStorage\"\n'); f.close()"
RUN cd /repo && poetry run python -c "f=open('heltour/settings_testing.py','w'); f.write('from .settings_default import *\nCACHEOPS = {\n    \"*.*\": {\"ops\": set(), \"timeout\": 0},\n}\nSTATICFILES_STORAGE = \"django.contrib.staticfiles.storage.StaticFilesStorage\"\n'); f.close()"
RUN cd /repo && poetry run pip list | grep -i openssl
RUN cd /repo && poetry run pip install -q pyOpenSSL==23.0.0