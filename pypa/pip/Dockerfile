FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/pypa/pip.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /pip/. /repo && rm -rf /pip/
RUN rm -rf /pip
RUN cd /repo && pip install -e . -q
RUN pip install installer==0.7.0
RUN pip install pytest==9.0.2
RUN pip install pytest-cov==7.0.0
RUN pip install pytest-rerunfailures==16.1
RUN pip install pytest-xdist==3.8.0
RUN pip install pytest-subket==0.8.2
RUN pip install scripttest==2.0.post1
RUN pip install cryptography==46.0.5
RUN pip install freezegun==1.5.5
RUN pip install werkzeug==3.1.6
RUN pip install tomli-w==1.2.0
RUN pip install proxy.py==2.4.10
RUN pip install virtualenv==21.0.0
RUN pip install flit-core==3.12.0