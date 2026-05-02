FROM python:3.10
WORKDIR /
COPY search_patch /search_patch
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/hazyresearch/meerkat.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /meerkat/. /repo && rm -rf /meerkat/
RUN rm -rf /meerkat
RUN find /repo -name "requirements*.txt" -o -name "pyproject.toml" -o -name "poetry.lock" 2>/dev/null
RUN cd /repo && pip install -e . -q
RUN python -c "import numpy; print(numpy.__version__)"
RUN python -c "import numpy.exceptions; print(dir(numpy.exceptions))"
RUN pip install -q torchvision==0.26.0 torchaudio==2.11.0
RUN for f in /repo/meerkat/interactive/app/src/lib/component/core/*/test_*.py; do sed -i 's/page.launch()/if __name__ == "__main__": page.launch()/g' "$f"; done
RUN for f in /repo/meerkat/interactive/app/src/lib/component/html/test_*.py; do sed -i 's/page.launch()/if __name__ == "__main__": page.launch()/g' "$f"; done
RUN for f in /repo/meerkat/interactive/app/src/lib/component/core/*/test_*.py /repo/meerkat/interactive/app/src/lib/component/html/test_*.py; do sed -i 's/if __name__ == "__main__": if __name__ == "__main__": page.launch()/if __name__ == "__main__": page.launch()/g' "$f"; done