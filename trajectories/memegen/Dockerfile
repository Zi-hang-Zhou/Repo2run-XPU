FROM python:3.12
WORKDIR /
COPY search_patch /search_patch
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/jacebrowning/memegen.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /memegen/. /repo && rm -rf /memegen/
RUN rm -rf /memegen
RUN cd /repo && poetry lock
RUN cd /repo && poetry add multidict --group dev
RUN cd /repo && poetry install