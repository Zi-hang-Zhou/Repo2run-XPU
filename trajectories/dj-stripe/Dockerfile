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
RUN find /repo -name "requirements*.txt" -o -name "setup.py" -o -name "setup.cfg" 2>/dev/null
RUN cd /repo && poetry install --with ci
RUN cd /repo && poetry run python -c "import django; print(django.__version__)"
RUN cd /repo && poetry env info
RUN cd /repo && poetry run pip list | head -30
RUN cd /repo && poetry install --with ci,dev
RUN cd /repo && poetry install --with ci,dev -E postgres
RUN cd /repo && poetry run pip index versions stripe --python-version 3.10 2>&1 | head -20
RUN cd /repo && poetry run pip install -q stripe==8.0.0