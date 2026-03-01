FROM python:3.13
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
RUN apt-get install -y -qq libgirepository1.0-dev libcairo2-dev pkg-config python3-dev gir1.2-glib-2.0
RUN apt-cache search girepository
RUN apt-get install -y -qq libgirepository-2.0-dev
RUN cd /repo && pip install -e . -q
RUN apt-get install -y -qq gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
RUN pip install -q pytest-mock==3.15.1 faker==40.5.1 dirty-equals==0.11 polyfactory==3.3.0 responses==0.26.0 pytest-cov==7.0.0