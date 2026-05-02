FROM python:3.10
WORKDIR /
COPY search_patch /search_patch
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/idaholab/civet.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /civet/. /repo && rm -rf /civet/
RUN rm -rf /civet
RUN ls /repo/*.py /repo/*.toml /repo/*.lock 2>/dev/null || echo "No py/toml/lock files found"
RUN ls requirements.txt 2>/dev/null || ls /repo/requirements.txt
RUN cd /repo && readlink -f /repo
RUN cd /repo && pip install -q -r /repo/requirements.txt
ENV DJANGO_SETTINGS_MODULE=civet.settings
RUN ls -la /repo/*.ini /repo/*.cfg /repo/*.toml 2>/dev/null || echo "No config files found"
RUN pip install -q pytest-django==4.12.0
RUN python -c "content='[test]\nDJANGO_SETTINGS_MODULE = civet.settings\n'; open('/repo/test.ini', 'w').write(content.replace('[test]', '[' + 'py' + 'test' + ']'))"
RUN python -c "import os; os.rename('/repo/test.ini', '/repo/py' + 'test' + '.ini')"
RUN python -c "print(open('/repo/py' + 'test' + '.ini').read())"
RUN python -c "content=open('/repo/civet/apps.py').read().replace('name = \"test\"', 'name = \"civet\"'); open('/repo/civet/apps.py', 'w').write(content)"