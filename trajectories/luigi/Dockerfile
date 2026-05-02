FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/spotify/luigi.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /luigi/. /repo && rm -rf /luigi/
RUN rm -rf /luigi
RUN find /repo -name "requirements*.txt" -o -name "Pipfile*" -o -name "pyproject.toml" 2>/dev/null
RUN cd /repo && pip install -e . -q
RUN pip install httpretty==0.8.10
RUN pip install docker==7.1.0
RUN pip install boto3==1.42.88
RUN pip install codecov==2.1.13
RUN pip install pygments==2.20.0
RUN pip install selenium==3.0.2
RUN pip install pymongo==3.4.0
RUN pip install datadog==0.22.0
RUN pip install jsonschema==4.26.0
RUN pip install avro-python3==1.10.2
RUN pip install google-compute-engine==2.8.13
RUN pip install mysql-connector-python==9.6.0
RUN pip install -q pytest-cov>=2.0,<3.0 mock<2.0 moto>=1.3.10,<5.0 boto>=2.42,<3.0 sqlalchemy<1.4 psutil<4.0 s3transfer>=0.3,<4.0 elasticsearch>=1.0.0,<2.0.0 coverage>=5.0,<6 requests>=2.20.0,<3.0 hypothesis>=6.7.0,<7.0.0 toml<2.0.0 responses<1.0.0 azure-storage<=0.36 prometheus-client>=0.5.0,<0.15 pytest<7.0
ENV AWS_DEFAULT_REGION=us-east-1
ENV AWS_ACCESS_KEY_ID=accesskey
ENV AWS_SECRET_ACCESS_KEY=secretkey
RUN pip install -q pyhive[presto]==0.6.1