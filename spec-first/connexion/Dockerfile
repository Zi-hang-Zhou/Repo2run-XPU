FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/spec-first/connexion.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /connexion/. /repo && rm -rf /connexion/
RUN rm -rf /connexion
RUN ls -la /repo/poetry.lock 2>/dev/null || echo "No poetry.lock found"
RUN cd /repo && poetry --version
RUN cd /repo && poetry lock
RUN cd /repo && poetry install --all-extras --with tests