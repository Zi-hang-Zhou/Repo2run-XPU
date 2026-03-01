FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/beeware/briefcase.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /briefcase/. /repo && rm -rf /briefcase/
RUN rm -rf /briefcase
RUN ls -la /repo/poetry.lock 2>/dev/null || echo "No poetry.lock found"
RUN find /repo -name "requirements*.txt" -type f 2>/dev/null
RUN cd /repo && pip install -e . -q
RUN pip install httpx-retries==0.4.6 pytest==9.0.2 pytest-xdist==3.8.0 coverage==7.13.4 coverage-conditional-plugin==0.9.0 -q
RUN pip show urllib3 requests
RUN pip install urllib3==2.2.0 -q
RUN pip install requests==2.31.0 -q
RUN pip install urllib3==1.26.18 -q
RUN pip install chardet==5.2.0 charset-normalizer==3.3.2 -q