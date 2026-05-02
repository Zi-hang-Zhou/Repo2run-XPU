FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/online-ml/river.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /river/. /repo && rm -rf /river/
RUN rm -rf /river
RUN pip install -q numpy==1.26.4 scipy==1.15.3 pandas==2.3.3 cython==3.2.4 setuptools-rust==1.12.1
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
RUN . "$HOME/.cargo/env"
RUN cd /repo && pip install -e . -q
RUN pip install -q scikit-learn==1.7.2 polars==1.39.3 sympy==1.14.0
RUN pip install -q gym==0.26.2