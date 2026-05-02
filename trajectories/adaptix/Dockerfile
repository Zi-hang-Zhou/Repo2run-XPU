FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/reagento/adaptix.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /adaptix/. /repo && rm -rf /adaptix/
RUN rm -rf /adaptix
RUN cd /repo && pip install -e . -q
RUN cd /repo/tests/tests_helpers && pip install -e . -q
RUN pip install -q dirty-equals==0.7.1.post0 phonenumberslite==8.13.26