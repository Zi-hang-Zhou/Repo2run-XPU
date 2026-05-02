FROM python:3.10
WORKDIR /
COPY search_patch /search_patch
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/columnflow/columnflow.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /columnflow/. /repo && rm -rf /columnflow/
RUN rm -rf /columnflow
RUN find /repo -name "requirements*.txt" -o -name "pyproject.toml" -o -name "poetry.lock" 2>/dev/null | head -20
RUN cd /repo && pip install -e . -q
RUN pip show luigi
RUN pip index versions law --python-version 3.10 2>&1 | head -10
RUN pip install law==0.1.20
ENV CF_WLCG_USE_CACHE=False
ENV CF_WLCG_USE_CACHE=False
ENV CF_WLCG_CACHE_CLEANUP=False
ENV CF_WLCG_CACHE_ROOT=/tmp
ENV CF_BASE=/repo
ENV CF_HTCONDOR_FLAVOR=default
ENV CF_SLURM_FLAVOR=default
ENV CF_SLURM_PARTITION=default
ENV CF_JOB_BASE=/tmp
ENV CF_CRAB_STORAGE_ELEMENT=default
ENV CF_CRAB_BASE_DIRECTORY=/tmp
ENV CF_CERN_USER=test
ENV CF_STORE_NAME=test
ENV CF_LOCAL_SCHEDULER=False
ENV CF_SCHEDULER_HOST=localhost
ENV CF_SCHEDULER_PORT=8080
ENV CF_WORKER_KEEP_ALIVE=False
RUN pip index versions order --python-version 3.10 2>&1 | head -10
RUN pip install order==2.1.7
ENV CF_WLCG_USE_CACHE=False
ENV CF_WLCG_CACHE_CLEANUP=False
ENV CF_WLCG_CACHE_ROOT=/tmp
ENV CF_BASE=/repo
ENV CF_HTCONDOR_FLAVOR=default
ENV CF_SLURM_FLAVOR=default
ENV CF_SLURM_PARTITION=default
ENV CF_JOB_BASE=/tmp
ENV CF_CRAB_STORAGE_ELEMENT=default
ENV CF_CRAB_BASE_DIRECTORY=/tmp
ENV CF_CERN_USER=test
ENV CF_STORE_NAME=test
ENV CF_LOCAL_SCHEDULER=False
ENV CF_SCHEDULER_HOST=localhost
ENV CF_SCHEDULER_PORT=8080
ENV CF_WORKER_KEEP_ALIVE=False
ENV CF_DEV=1
RUN pip install awkward==2.9.0
ENV CF_WLCG_USE_CACHE=False
ENV CF_WLCG_CACHE_CLEANUP=False
ENV CF_WLCG_CACHE_ROOT=/tmp
ENV CF_BASE=/repo
ENV CF_HTCONDOR_FLAVOR=default
ENV CF_SLURM_FLAVOR=default
ENV CF_SLURM_PARTITION=default
ENV CF_JOB_BASE=/tmp
ENV CF_CRAB_STORAGE_ELEMENT=default
ENV CF_CRAB_BASE_DIRECTORY=/tmp
ENV CF_CERN_USER=test
ENV CF_STORE_NAME=test
ENV CF_LOCAL_SCHEDULER=False
ENV CF_SCHEDULER_HOST=localhost
ENV CF_SCHEDULER_PORT=8080
ENV CF_WORKER_KEEP_ALIVE=False
ENV CF_DEV=1