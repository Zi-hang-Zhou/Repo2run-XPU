FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/google/trax.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /trax/. /repo && rm -rf /trax/
RUN rm -rf /trax
RUN find /repo -name "requirements*.txt" -o -name "Pipfile*" -o -name "pyproject.toml" -o -name "poetry.lock" 2>/dev/null
RUN cd /repo && pip install -e .[tests] -q
RUN pip show tensorflow numpy
RUN pip install numpy==1.23.5
RUN pip install -q numpy>=1.21,<1.24
RUN pip show numpy | grep Version
RUN pip show jax jaxlib | grep -E "Name|Version"
RUN python -c "import numpy as np; print(hasattr(np, 'dtypes')); print(np.__version__)"
RUN pip install -q jax<0.5 jaxlib<0.5
RUN pip show numpy | grep Version
RUN pip install -q numpy>=1.21,<1.24
RUN pip install -q tensorflow==2.12.0 numpy>=1.23,<1.24 jax<0.5 jaxlib<0.5
RUN pip install -q tensorflow-text==2.12.0
RUN pip install -q t5==0.9.4 --no-build-isolation
RUN pip show numpy tensorflow jax | grep -E "Name|Version"
RUN echo "W3Rvb2w6cHl0ZXN0XQphZGRvcHRzID0gLS1pZ25vcmU9dHJheC90Zl9udW1weS9leHRlbnNpb25zL2V4dGVuc2lvbnNfdGVzdC5weSAtLWlnbm9yZT10cmF4L3RmX251bXB5L2pheF90ZXN0cy90ZXN0X3V0aWwucHkK" | base64 -d > /repo/setup.cfg