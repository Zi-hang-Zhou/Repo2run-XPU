FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/robotframework/robotframework.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /robotframework/. /repo && rm -rf /robotframework/
RUN rm -rf /robotframework
RUN cd /repo && pip install -e . -q
RUN cd /repo && pip install -r /repo/utest/requirements.txt -q
RUN cd /repo && pip install -r /repo/atest/requirements.txt -q
RUN cd /repo && pip install -r /repo/atest/requirements-run.txt -q
ENV PYTHONPATH=/repo/utest/resources:/repo/atest/testresources/testlibs:$PYTHONPATH
ENV PYTHONPATH=/repo/utest:/repo/atest/testresources/testlibs:$PYTHONPATH