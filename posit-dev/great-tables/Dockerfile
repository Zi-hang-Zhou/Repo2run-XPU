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
RUN cd /repo && pip install -e . -q
RUN pip install -q pytest-cov==7.0.0
RUN pip install numpy==2.2.6
RUN pip install pandas==2.3.3
RUN pip install selenium==4.41.0
RUN pip install polars==1.38.1
RUN pip install requests==2.32.5
RUN pip install ipykernel==7.2.0
RUN pip install pyarrow==23.0.1