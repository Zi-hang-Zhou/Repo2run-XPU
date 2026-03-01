FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/pypa/twine.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /twine/. /repo && rm -rf /twine/
RUN rm -rf /twine
RUN find /repo -name "requirements*.txt" -o -name "Pipfile*" -o -name "poetry.lock" 2>/dev/null
RUN cd /repo && pip install -e . -q
RUN pip install pytest-socket==0.7.0 -q
RUN pip install pretend==1.0.9 -q