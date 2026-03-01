FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/mampfes/hacs_waste_collection_schedule.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /hacs_waste_collection_schedule/. /repo && rm -rf /hacs_waste_collection_schedule/
RUN rm -rf /hacs_waste_collection_schedule
RUN ls -la /repo/*.toml /repo/*.py 2>/dev/null | head -20
RUN pip install beautifulsoup4==4.14.3
RUN pip install cloudscraper==1.2.71
RUN pip install datetime==6.0
RUN pip install icalendar==7.0.2
RUN pip install icalevents==0.3.1
RUN pip install python-dateutil==2.9.0.post0
RUN pip install pytz==2025.2
RUN pip install pyyaml==6.0.1
RUN pip install requests==2.31.0
RUN pip install urllib3==2.6.3
RUN pip install jinja2==3.1.2
RUN pip install lxml==6.0.2
RUN pip install pycryptodome==3.23.0
RUN pip install typing_extensions==4.15.0
RUN pip install pypdf==6.7.3
RUN pip install homeassistant==2023.7.3