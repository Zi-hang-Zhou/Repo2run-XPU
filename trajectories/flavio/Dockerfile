FROM python:3.10
WORKDIR /
COPY search_patch /search_patch
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/flav-io/flavio.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /flavio/. /repo && rm -rf /flavio/
RUN rm -rf /flavio
RUN find /repo -name "requirements*.txt" -o -name "pyproject.toml" -o -name "poetry.lock" 2>/dev/null
RUN cat /repo/.github/workflows/*.yml 2>/dev/null || cat /repo/.github/workflows/*.yaml 2>/dev/null
RUN cd /repo && pip install -e .[sampling,plotting,testing] -q
RUN pip show scipy
RUN python -c "import scipy.integrate; print(dir(scipy.integrate))" | grep -i warn
RUN sed -i 's/from scipy.integrate.quadrature import AccuracyWarning # scipy <= 1.4.1/try:\n        from scipy.integrate.quadrature import AccuracyWarning # scipy <= 1.4.1\n    except ImportError:\n        from scipy.integrate import IntegrationWarning as AccuracyWarning # scipy >= 1.14/' /repo/flavio/math/integrate.py