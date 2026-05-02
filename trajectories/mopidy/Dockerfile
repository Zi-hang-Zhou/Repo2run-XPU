FROM python:3.11
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/mopidy/mopidy.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /mopidy/. /repo && rm -rf /mopidy/
RUN rm -rf /mopidy
RUN apt-get update -qq
RUN apt-get install -y -qq libgirepository1.0-dev python3-gi python3-gi-cairo gir1.2-glib-2.0
RUN apt-cache search girepository
RUN apt-get install -y -qq libgirepository-2.0-dev
RUN cd /repo && pip install -e . -q
RUN apt-get install -y -qq gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-tools gir1.2-gst-1.0
RUN pip install -q pytest==9.0.3 pytest-cov==7.1.0 responses==0.26.0
RUN apt-get install -y -qq libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev