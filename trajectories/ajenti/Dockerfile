FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/ajenti/ajenti.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /ajenti/. /repo && rm -rf /ajenti/
RUN rm -rf /ajenti
RUN find /repo -name "setup.py" -o -name "requirements*.txt" 2>/dev/null | head -20
RUN find /repo -name "setup.py" 2>/dev/null
RUN cat /repo/.github/workflows/*.yml 2>/dev/null | head -100
RUN find /repo -name "test*.py" -o -name "*_test.py" 2>/dev/null | head -20
RUN pip install -q pipreqs==0.5.0
RUN cd /repo && pipreqs . --savepath requirements_pipreqs.txt --force
RUN cd /repo && pip install -q requests==2.33.1 pytest==9.0.3