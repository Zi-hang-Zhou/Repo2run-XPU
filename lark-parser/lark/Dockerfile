FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/lark-parser/lark.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /lark/. /repo && rm -rf /lark/
RUN rm -rf /lark