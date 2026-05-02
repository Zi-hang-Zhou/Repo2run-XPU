FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/pypose/pypose.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /pypose/. /repo && rm -rf /pypose/
RUN rm -rf /pypose
RUN ls -la /repo/*.toml /repo/*.lock 2>/dev/null; ls -la /repo/.github/
RUN cat /repo/.github/workflows/*.yml 2>/dev/null | head -100
RUN pip install pytest==9.0.3
RUN pip install torch==2.11.0
RUN cd /repo && pip install -e . -q
RUN pip install torchvision==0.26.0