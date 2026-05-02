FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/conda-forge/staged-recipes.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /staged-recipes/. /repo && rm -rf /staged-recipes/
RUN rm -rf /staged-recipes
RUN find /repo -name "requirements*.txt" -o -name "pyproject.toml" -o -name "setup.py" 2>/dev/null
RUN find /repo -name "test*.py" -o -name "*_test.py" 2>/dev/null
RUN find /repo -name "*.py" -type f 2>/dev/null | head -20