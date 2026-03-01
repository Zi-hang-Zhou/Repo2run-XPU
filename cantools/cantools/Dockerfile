FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/cantools/cantools.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /cantools/. /repo && rm -rf /cantools/
RUN rm -rf /cantools
RUN ls -la /repo/*.lock /repo/requirements*.txt 2>/dev/null; ls -la /repo/tests/
RUN cd /repo && pip install -e . -q
RUN pip install parameterized==0.9.0 freezegun==1.5.5 matplotlib==3.10.8 -q