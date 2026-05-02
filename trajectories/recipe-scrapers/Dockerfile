FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/hhursev/recipe-scrapers.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /recipe-scrapers/. /repo && rm -rf /recipe-scrapers/
RUN rm -rf /recipe-scrapers
RUN cd /repo && pip install -e . -q
RUN pip install responses==0.26.0 coverage==7.13.5 types-beautifulsoup4==4.12.0.20250516 types-requests==2.33.0.20260408 -q