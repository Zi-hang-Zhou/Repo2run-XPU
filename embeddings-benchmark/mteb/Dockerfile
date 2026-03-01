FROM python:3.10
WORKDIR /
COPY search_patch /search_patch
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/embeddings-benchmark/mteb.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /mteb/. /repo && rm -rf /mteb/
RUN rm -rf /mteb
RUN ls -la /repo/*.lock /repo/*.txt 2>/dev/null; ls -la /repo/.github/
RUN cat /repo/.github/workflows/*.yml 2>/dev/null | head -200
RUN cd /repo && pip install -e . -q
RUN cd /repo && pip install pytest-rerunfailures==16.1 pytest-xdist==3.8.0 pytest-coverage==0.0 iso639==0.1.4 GitPython==3.1.46 tabulate==0.9.0 -q
RUN pip install bibtexparser==1.4.4 -q