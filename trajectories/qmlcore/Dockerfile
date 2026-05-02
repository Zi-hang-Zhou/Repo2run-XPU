FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/pureqml/qmlcore.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /qmlcore/. /repo && rm -rf /qmlcore/
RUN rm -rf /qmlcore
RUN ls /repo/*.py /repo/*.toml 2>/dev/null; cat /repo/test/lit.cfg.py
RUN pip install future==1.0.0
RUN pip install pyparsing==3.3.2