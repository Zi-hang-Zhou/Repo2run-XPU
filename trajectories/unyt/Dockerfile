FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/yt-project/unyt.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /unyt/. /repo && rm -rf /unyt/
RUN rm -rf /unyt
RUN find /repo -name "requirements*.txt" -o -name "Pipfile*" -o -name "poetry.lock" 2>/dev/null
RUN cd /repo && pip install -e . -q
RUN pip install pytest==9.0.3
RUN pip install h5py==3.16.0
RUN pip install pint==0.24.4
RUN pip install astropy==6.1.7
RUN pip install coverage==7.13.5
RUN pip install pytest-cov==7.1.0
RUN pip install pytest-doctestplus==1.7.1
RUN pip install matplotlib==3.10.8
RUN pip install docutils==0.22.4
RUN pip install dask==2026.3.0