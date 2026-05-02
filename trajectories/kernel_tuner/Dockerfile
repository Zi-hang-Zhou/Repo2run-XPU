FROM python:3.10
WORKDIR /
COPY search_patch /search_patch
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/kerneltuner/kernel_tuner.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /kernel_tuner/. /repo && rm -rf /kernel_tuner/
RUN rm -rf /kernel_tuner
RUN find /repo -name "requirements*.txt" -o -name "Pipfile*" -o -name "environment.yml" 2>/dev/null
RUN cd /repo && pip install -e . -q
RUN pip install pytest-cov==7.1.0 -q