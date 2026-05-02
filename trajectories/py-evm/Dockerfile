FROM python:3.10
WORKDIR /
COPY search_patch /search_patch
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/ethereum/py-evm.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /py-evm/. /repo && rm -rf /py-evm/
RUN rm -rf /py-evm
RUN ls -la /repo/*.lock 2>/dev/null || echo "No lock files found"
RUN find /repo -name "requirements*.txt" -type f 2>/dev/null
RUN cd /repo && pip install -e .[test,eth-extra] -q
RUN cd /repo && git submodule update --init --recursive
RUN pip index versions ethereum-test-forks --python-version 3.10 2>&1 | head -5 || pip search ethereum-test-forks 2>&1 | head -10 || pip install ethereum-test-forks -q 2>&1 | head -10
RUN pip index versions ethereum-spec-evm-resolver --python-version 3.10 2>&1 | head -5
RUN pip index versions ethereum-execution-spec-tests --python-version 3.10 2>&1 | head -5
RUN pip install -q git+https://github.com/ethereum/execution-spec-tests.git 2>&1 | head -20