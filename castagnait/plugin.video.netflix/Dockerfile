FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/castagnait/plugin.video.netflix.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /plugin.video.netflix/. /repo && rm -rf /plugin.video.netflix/
RUN rm -rf /plugin.video.netflix
RUN ls -la /repo/*.py /repo/*.toml /repo/*.lock 2>/dev/null || echo "No toml or lock files found"
RUN cat /repo/.github/workflows/*.yml 2>/dev/null | head -100
RUN ls -la /repo/resources/lib 2>/dev/null || echo "No lib folder"