FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/datamol-io/datamol.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /datamol/. /repo && rm -rf /datamol/
RUN rm -rf /datamol
RUN ls /repo/*.txt 2>/dev/null || echo "No .txt files in root"
RUN ls /repo/setup.py 2>/dev/null || echo "No setup.py"
RUN cd /repo && pip install -e . -q
RUN pip install -q pytest-cov==7.1.0 pytest-xdist==3.8.0
RUN pip install -q nbformat==5.10.4 ipywidgets==8.1.8
RUN pip install -q nbconvert==7.17.1