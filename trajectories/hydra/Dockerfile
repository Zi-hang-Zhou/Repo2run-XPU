FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/facebookresearch/hydra.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /hydra/. /repo && rm -rf /hydra/
RUN rm -rf /hydra
RUN python /home/tools/apt_download.py -p default-jre
RUN pip install omegaconf==2.4.0.dev4
RUN pip install packaging==26.0
RUN pip show omegaconf
RUN pip index versions antlr4-python3-runtime --python-version 3.10
RUN python -c "import omegaconf; print(omegaconf.__file__)"
RUN pip index versions omegaconf --python-version 3.10
RUN python -c "from antlr4.error.Errors import LexerNoViableAltException; print('antlr4 works directly')"
RUN pip install -q setuptools==79.0.1
RUN pip install -q --no-build-isolation git+https://github.com/omry/omegaconf.git
RUN python -c "from omegaconf.vendor.antlr4.error.Errors import LexerNoViableAltException; print('vendor antlr4 works')"
RUN cd /repo && python setup.py antlr
RUN pip show pytest
RUN pip index versions pytest --python-version 3.10 | head -20
RUN pip install -q pytest==7.4.4