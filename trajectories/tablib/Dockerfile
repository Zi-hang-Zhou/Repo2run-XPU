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
RUN pip install pytest==9.0.3
RUN pip install pytest-cov==7.1.0
RUN pip install odfpy==1.4.1
RUN pip install openpyxl==3.1.5
RUN pip install pyyaml==6.0.3
RUN pip install tabulate==0.10.0
RUN pip install xlrd==2.0.2
RUN pip install xlwt==1.3.0
RUN cd /repo && pip install -e . -q