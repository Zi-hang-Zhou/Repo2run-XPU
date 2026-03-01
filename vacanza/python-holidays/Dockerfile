FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/vacanza/python-holidays.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /python-holidays/. /repo && rm -rf /python-holidays/
RUN rm -rf /python-holidays
RUN find /repo -name "requirements*.txt" -o -name "setup.py" 2>/dev/null | head -20
RUN cd /repo && pip install -e . -q
RUN pip install pytest-cov==7.0.0 pytest-xdist==3.8.0 coverage==7.13.4 -q
RUN pip install polib==1.2.0
RUN pip install numpy==2.2.6