FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/nixtla/neuralforecast.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /neuralforecast/. /repo && rm -rf /neuralforecast/
RUN rm -rf /neuralforecast
RUN ls -la /repo/*.lock /repo/requirements*.txt 2>/dev/null; echo "---"; ls -la /repo/test/
RUN pip install setuptools==79.0.1 -q
RUN cd /repo && pip install -e . --no-build-isolation -q
RUN pip install matplotlib==3.10.8