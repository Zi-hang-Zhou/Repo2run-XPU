FROM python:3.10
WORKDIR /
COPY search_patch /search_patch
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/emi-group/evox.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /evox/. /repo && rm -rf /evox/
RUN rm -rf /evox
RUN cd /repo && pip install -e . -q
RUN pip install chex==0.1.90
RUN pip install flax==0.8.5
RUN pip install gymnasium==1.2.3
RUN pip install ray==2.54.1
RUN pip install tensorflow-datasets==4.9.9
RUN pip install grain==0.2.13
RUN pip install envpool==0.8.4
RUN pip install gpjax==0.8.2
RUN pip show jax | grep Version
RUN pip install jax==0.4.25 jaxlib==0.4.25 -q
RUN pip install jax==0.4.30 jaxlib==0.4.30 -q
RUN pip index versions envpool --python-version 3.10
RUN pip install jax>=0.6.0 jaxlib>=0.6.0 -q
RUN pip show flax | grep Version
RUN cd /repo && git checkout src/evox/algorithms/mo/im_moea.py
RUN cd /repo && pip index versions flax --python-version 3.10 | head -20
RUN cd /repo && pip install flax==0.8.5 -q
RUN cd /repo && pip index versions gpjax --python-version 3.10 | head -20
RUN cd /repo && pip install gpjax==0.8.2 flax==0.8.5 jax==0.4.30 jaxlib==0.4.30 -q