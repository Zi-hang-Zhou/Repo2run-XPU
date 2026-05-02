FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/fabric/fabric.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /fabric/. /repo && rm -rf /fabric/
RUN rm -rf /fabric
RUN cd /repo && pip install -e . -q
RUN pip install icecream==2.2.0
RUN pip install invoke==3.0.3
RUN pip install invocations==4.0.2
RUN pip install pytest-relaxed==2.0.2
RUN pip install pytest-cov==7.1.0
RUN pip install flake8==4.0.1
RUN pip install black==22.8.0
RUN pip install coverage==6.5.0
RUN pip install releases==2.1.1
RUN pip install alabaster==0.7.13