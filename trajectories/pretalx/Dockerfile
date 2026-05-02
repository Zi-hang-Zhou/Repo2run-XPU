FROM python:3.10
WORKDIR /
COPY search_patch /search_patch
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/pretalx/pretalx.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /pretalx/. /repo && rm -rf /pretalx/
RUN rm -rf /pretalx
RUN find /repo -name "requirements*.txt" -o -name "poetry.lock" -o -name "Pipfile*" 2>/dev/null
RUN cd /repo && pip install -e . -q
ENV DJANGO_SETTINGS_MODULE=pretalx.common.settings.test_settings
RUN pip list | grep -i django
RUN pip install pytest-django==4.12.0 pytest-cov==7.1.0 pytest-mock==3.15.1 pytest-rerunfailures==16.1 pytest-sugar==1.1.1 pytest-xdist==3.8.0 freezegun==1.5.5 responses==0.26.0 Faker==40.13.0 coverage==7.13.5 -q
RUN cd /repo/src && ls -la /repo/tests 2>/dev/null || echo "No tests in /repo"
RUN cd /repo && echo "import os" > conftest.py
RUN cd /repo && echo "os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pretalx.common.settings.test_settings')" >> conftest.py
RUN cd /repo && echo "import django" >> conftest.py
RUN cd /repo && echo "django.setup()" >> conftest.py
RUN pip install jsonschema==4.26.0 -q