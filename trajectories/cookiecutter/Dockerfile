FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/cookiecutter/cookiecutter.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /cookiecutter/. /repo && rm -rf /cookiecutter/
RUN rm -rf /cookiecutter
RUN cd /repo && pip install -e . -q
RUN pip install freezegun==1.5.5
RUN pip install safety==3.7.0
RUN pip install pre-commit==4.5.1
RUN pip install tox==4.52.1
RUN pip install pytest-cov==7.1.0 pytest-mock==3.15.1 -q