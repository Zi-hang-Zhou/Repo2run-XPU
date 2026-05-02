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
RUN cd /repo && pip install -e . -q
RUN cd /repo && pip install piccolo[postgres] -q
RUN cd /repo && pip install -r requirements/extras/sqlite.txt -q
RUN cd /repo && pip install -r requirements/test-requirements.txt -q
ENV PICCOLO_CONF="tests.sqlite_conf"