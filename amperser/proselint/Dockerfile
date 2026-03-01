FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/amperser/proselint.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /proselint/. /repo && rm -rf /proselint/
RUN rm -rf /proselint
RUN find /repo -name "requirements*.txt" -o -name "Pipfile*" 2>/dev/null
RUN cat /repo/.github/workflows/*.yml 2>/dev/null || cat /repo/.github/workflows/*.yaml 2>/dev/null
RUN pip install google-re2==1.1.20251105
RUN pip install google-re2-stubs==0.1.1
RUN pip install hypothesis==6.151.9
RUN pip install pytest==9.0.2
RUN pip install pytest-cov==7.0.0
RUN pip install rstr==3.2.2
RUN cd /repo && pip install -e . -q