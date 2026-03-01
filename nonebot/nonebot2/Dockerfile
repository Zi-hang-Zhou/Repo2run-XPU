FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/nonebot/nonebot2.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /nonebot2/. /repo && rm -rf /nonebot2/
RUN rm -rf /nonebot2
RUN find /repo -name "requirements*.txt" -o -name "setup.py" 2>/dev/null | head -20
RUN cd /repo && pip install -e . -q
RUN pip install trio==0.33.0
RUN pip install -q nonebug>=0.4.1,<0.5.0 wsproto>=1.2.0,<2.0.0 werkzeug>=2.3.6,<4.0.0 pytest-cov>=7.0.0,<8.0.0 pytest-xdist>=3.0.2,<4.0.0 coverage-conditional-plugin>=0.9.0,<0.10.0