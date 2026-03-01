FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/dj-stripe/dj-stripe.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /dj-stripe/. /repo && rm -rf /dj-stripe/
RUN rm -rf /dj-stripe
RUN cd /repo && poetry --version
RUN cd /repo && poetry install --with dev,ci -q