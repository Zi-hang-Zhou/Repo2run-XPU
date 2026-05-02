FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/tommadness/kh2randomizer.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /kh2randomizer/. /repo && rm -rf /kh2randomizer/
RUN rm -rf /kh2randomizer
RUN ls /repo/*.toml /repo/*.py 2>/dev/null | head -20
RUN find /repo -name "pyproject.toml" -o -name "setup.py" -o -name "setup.cfg" 2>/dev/null
RUN pip install -q altgraph==0.17.2
RUN pip install -q bitstring==3.1.9 future==0.18.2 khbr==4.0.5 numpy==1.25.2 pefile==2021.9.3
RUN pip install -q pillow==9.3.0
RUN pip install -q pyperclip==1.8.2 pytz==2021.3 pywin32-ctypes==0.2.0 requests==2.31.0 tomlkit==0.11.1
RUN pip index versions PyYAML --python-version 3.10 2>/dev/null | head -10
RUN pip install -q pyinstaller==4.5.1 pyinstaller-hooks-contrib==2024.1
RUN pip install -q PySide6==6.2.1 shiboken6==6.2.1