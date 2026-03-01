FROM python:3.14
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/tmux-python/tmuxp.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /tmuxp/. /repo && rm -rf /tmuxp/
RUN rm -rf /tmuxp
RUN find /repo -name "requirements*.txt" -o -name "poetry.lock" 2>/dev/null | head -20
RUN cd /repo && pip install -e . -q
RUN pip install pytest-rerunfailures==16.1 -q
RUN pip install docutils==0.22.4 -q
RUN pip install sphinx==9.1.0 -q