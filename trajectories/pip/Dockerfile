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
RUN find /repo -name "requirements*.txt" -o -name "requirements*.in" 2>/dev/null | head -20
RUN cd /repo && pip install -e . -q
RUN pip install virtualenv==21.2.1
RUN pip install cryptography==46.0.7
RUN pip install freezegun==1.5.5
RUN pip install installer==1.0.0
RUN pip install scripttest==2.0.post1
RUN pip install setuptools==79.0.1
RUN pip install werkzeug==3.1.8
RUN pip install wheel==0.45.1
RUN pip install tomli-w==1.2.0
RUN pip install proxy.py==2.4.10