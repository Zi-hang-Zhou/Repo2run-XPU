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
RUN find /repo -name "requirements*.txt" -type f 2>/dev/null
RUN cd /repo && pip install -e .[test,eth-extra] -q
RUN cd /repo && git submodule update --init --recursive
RUN cd /repo && python -c "from eth.tools.fixtures.loading import find_fixtures; fixtures = list(find_fixtures('/repo/fixtures/LegacyTests/Cancun/BlockchainTests')); print(f'Found {len(fixtures)} fixtures'); print(fixtures[:3] if fixtures else 'None')"
RUN cd /repo && python -c "from eth.tools.fixtures.loading import find_fixtures; print(len(list(find_fixtures('/repo/fixtures_eest/blockchain_tests'))))"