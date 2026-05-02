FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/cherrypy/cheroot.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /cheroot/. /repo && rm -rf /cheroot/
RUN rm -rf /cheroot
RUN cd /repo && pip install -e . -q
RUN pip install pytest==9.0.3 pytest-xdist==3.8.0 pytest-cov==7.1.0 pytest-mock==3.15.1 coverage==7.13.5 -q
RUN pip install jaraco.text==4.2.0 requests==2.33.1 pyopenssl==26.0.0 portend==3.2.1 -q
RUN pip install requests-unixsocket==0.4.1 trustme==1.2.1 requests-toolbelt==1.0.0 -q
RUN pip install pytest-rerunfailures==16.1 -q
RUN pip install pypytools==0.6.2 -q