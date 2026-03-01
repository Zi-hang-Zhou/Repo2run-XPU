FROM python:3.10
WORKDIR /
COPY search_patch /search_patch
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/roboflow/supervision.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /supervision/. /repo && rm -rf /supervision/
RUN rm -rf /supervision
RUN find /repo -name "requirements*.txt" -type f 2>/dev/null
RUN cd /repo && pip install -e . -q
RUN apt-get update -qq
RUN apt-cache search libgl | head -20
RUN apt-cache search libgl1
RUN apt-get install libgl1 libglib2.0-0 -y -qq