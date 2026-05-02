FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/sphinx-gallery/sphinx-gallery.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /sphinx-gallery/. /repo && rm -rf /sphinx-gallery/
RUN rm -rf /sphinx-gallery
RUN find /repo -name "requirements*.txt" -o -name "poetry.lock" 2>/dev/null
RUN cd /repo && pip install -e . -q
RUN pip install pytest-cov==7.1.0
RUN pip install pytest==9.0.3
RUN pip install numpy==2.2.6
RUN pip install matplotlib==3.10.8
RUN pip install pillow==12.2.0
RUN pip install seaborn==0.13.2
RUN pip install joblib==1.5.3
RUN pip install lxml==6.0.3