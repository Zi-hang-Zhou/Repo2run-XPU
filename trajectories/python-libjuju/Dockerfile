FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/juju/python-libjuju.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /python-libjuju/. /repo && rm -rf /python-libjuju/
RUN rm -rf /python-libjuju
RUN find /repo -name "requirements*.txt" -o -name "pyproject.toml" -o -name "poetry.lock" 2>/dev/null
RUN cd /repo && pip install -e . -q
RUN pip install -q mock==5.2.0 pytest==9.0.3 pytest-asyncio==1.3.0 pytest-xdist==3.8.0 ipdb==0.13.13 Twine==6.2.0 pylxd==2.4.1