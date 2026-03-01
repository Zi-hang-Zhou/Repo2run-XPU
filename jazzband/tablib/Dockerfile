FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/jazzband/tablib.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /tablib/. /repo && rm -rf /tablib/
RUN rm -rf /tablib
RUN find /repo -name "requirements*.txt" -o -name "setup.py" 2>/dev/null
RUN cd /repo && pip install -e . -q
RUN cd /repo && pip install -q odfpy==1.4.1 openpyxl>=2.6.0 pytest==9.0.2 pytest-cov==7.0.0 pyyaml==6.0.3 tabulate==0.9.0 xlrd==2.0.2 xlwt==1.3.0