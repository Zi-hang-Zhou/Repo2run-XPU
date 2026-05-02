FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/yubico/yubikey-manager.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /yubikey-manager/. /repo && rm -rf /yubikey-manager/
RUN rm -rf /yubikey-manager
RUN apt-get update -qq
RUN apt-get install -y -qq libpcsclite-dev swig
RUN cd /repo && poetry install