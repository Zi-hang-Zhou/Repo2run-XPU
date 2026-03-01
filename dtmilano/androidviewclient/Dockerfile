FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/dtmilano/androidviewclient.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /androidviewclient/. /repo && rm -rf /androidviewclient/
RUN rm -rf /androidviewclient
RUN cd /repo && pip install -e . -q
RUN pip install hypothesis==6.151.9
RUN pip install pytest-asyncio==1.3.0
RUN pip install responses==0.26.0
RUN pip install pytest==9.0.2