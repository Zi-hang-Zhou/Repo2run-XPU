FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/terrapower/armi.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /armi/. /repo && rm -rf /armi/
RUN rm -rf /armi
RUN find /repo -name "requirements*.txt" -o -name "setup.py" 2>/dev/null | head -20
RUN cd /repo && pip install -e . -q
RUN ls -la /repo/conftest.py 2>/dev/null || echo "No conftest.py in root"
RUN cd /repo && pip install -e .[test] -q
RUN cd /repo && python -c "import base64; open('/tmp/create_conftest.py','wb').write(base64.b64decode('aW1wb3J0IG9zCmltcG9ydCBtYXRwbG90bGliCmZyb20gYXJtaSBpbXBvcnQgYXBwcywgY29uZmlndXJlLCBjb250ZXh0CmZyb20gYXJtaS5zZXR0aW5ncyBpbXBvcnQgY2FzZVNldHRpbmdzCmZyb20gYXJtaS50ZXN0cyBpbXBvcnQgVEVTVF9ST09UCgpkZWYgcHl0ZXN0X3Nlc3Npb25zdGFydChzZXNzaW9uKToKICAgIHByaW50KCJJbml0aWFsaXppbmcgZ2VuZXJpYyBBUk1JIEZyYW1ld29yayBhcHBsaWNhdGlvbiIpCiAgICBjb25maWd1cmUoYXBwcy5BcHAoKSkKICAgIGJvb3RzdHJhcEFybWlUZXN0RW52KCkKCmRlZiBib290c3RyYXBBcm1pVGVzdEVudigpOgogICAgZnJvbSBhcm1pLm51Y0RpcmVjdG9yeSBpbXBvcnQgbnVjbGlkZUJhc2VzCiAgICBjcyA9IGNhc2VTZXR0aW5ncy5TZXR0aW5ncygpCiAgICBjb250ZXh0Lk1vZGUuc2V0TW9kZShjb250ZXh0Lk1vZGUuQkFUQ0gpCiAgICB3aXRoIG9wZW4oY3NbImJ1cm5DaGFpbkZpbGVOYW1lIl0pIGFzIGJ1cm5DaGFpblN0cmVhbToKICAgICAgICBudWNsaWRlQmFzZXMuaW1wb3NlQnVybkNoYWluKGJ1cm5DaGFpblN0cmVhbSkKICAgIG1hdHBsb3RsaWIudXNlKCJhZ2ciKQogICAgY29udGV4dC5hY3RpdmF0ZUxvY2FsRmFzdFBhdGgoKQogICAgaWYgbm90IG9zLnBhdGguZXhpc3RzKGNvbnRleHQuZ2V0RmFzdFBhdGgoKSk6CiAgICAgICAgb3MubWFrZWRpcnMoY29udGV4dC5nZXRGYXN0UGF0aCgpKQogICAgb3MuZW52aXJvblsiQVJNSVRFU1RCQVNFIl0gPSBURVNUX1JPT1QK'))"
RUN cd /repo && python /tmp/create_conftest.py
RUN cd /repo && cp /tmp/create_conftest.py /repo/conftest.py