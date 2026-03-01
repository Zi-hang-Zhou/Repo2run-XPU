FROM python:3.11
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
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
RUN source $HOME/.cargo/env
RUN cd /repo && pip install -e . -q
RUN find /repo -name "requirements*.txt" -type f 2>/dev/null
RUN pip install scikit-learn==1.8.0
RUN pip install polars==1.38.1
RUN pip install sympy==1.14.0
RUN pip install gymnasium==1.2.3