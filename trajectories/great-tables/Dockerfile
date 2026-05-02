FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/posit-dev/great-tables.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /great-tables/. /repo && rm -rf /great-tables/
RUN rm -rf /great-tables
RUN ls -la /repo/*.lock /repo/*.txt 2>/dev/null; ls -la /repo/tests/
RUN cd /repo && pip install -e . -q
RUN pip install pytest-cov==7.1.0 -q
RUN pip install pandas==2.3.3 requests==2.33.1 polars==1.39.3 shiny -q
RUN pip install IPython==8.39.0 -q
RUN pip install ipykernel==7.2.0 -q