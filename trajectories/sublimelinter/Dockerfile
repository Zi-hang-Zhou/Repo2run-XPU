FROM python:3.10
WORKDIR /
COPY search_patch /search_patch
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/sublimelinter/sublimelinter.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /sublimelinter/. /repo && rm -rf /sublimelinter/
RUN rm -rf /sublimelinter
RUN ls -la /repo/setup.py 2>/dev/null || echo "No setup.py"
RUN find /repo -name "sublime.py" 2>/dev/null
RUN pip install jsonschema==3.2.0
RUN pip install -q SublimeText-UnitTesting 2>/dev/null || echo Not found on PyPI
RUN pip search unittesting 2>/dev/null || pip index versions unittesting 2>/dev/null || echo "Checking alternatives"
RUN mkdir -p /repo/mocks
RUN echo 'import unittest' > /repo/mocks/unittesting.py
RUN echo '' >> /repo/mocks/unittesting.py
RUN echo 'class DeferrableTestCase(unittest.TestCase):' >> /repo/mocks/unittesting.py
RUN echo '    pass' >> /repo/mocks/unittesting.py
RUN echo '' >> /repo/mocks/unittesting.py
RUN echo 'AWAIT_WORKER = None' >> /repo/mocks/unittesting.py
RUN echo 'class Region:' > /repo/mocks/sublime.py
RUN echo '    def __init__(self, a, b=None):' >> /repo/mocks/sublime.py
RUN echo '        self.a = a' >> /repo/mocks/sublime.py
RUN echo '        self.b = b if b is not None else a' >> /repo/mocks/sublime.py
RUN echo '    def __repr__(self):' >> /repo/mocks/sublime.py
RUN echo '        return f"Region({self.a}, {self.b})"' >> /repo/mocks/sublime.py
RUN echo '' >> /repo/mocks/sublime.py
RUN echo 'class View:' >> /repo/mocks/sublime.py
RUN echo '    def __init__(self):' >> /repo/mocks/sublime.py
RUN echo '        pass' >> /repo/mocks/sublime.py
RUN echo '    def set_scratch(self, flag):' >> /repo/mocks/sublime.py
RUN echo '        pass' >> /repo/mocks/sublime.py
RUN echo '    def close(self):' >> /repo/mocks/sublime.py
RUN echo '        pass' >> /repo/mocks/sublime.py
RUN echo '' >> /repo/mocks/sublime.py
RUN echo 'class Window:' >> /repo/mocks/sublime.py
RUN echo '    def new_file(self):' >> /repo/mocks/sublime.py
RUN echo '        return View()' >> /repo/mocks/sublime.py
RUN echo '    def focus_view(self, view):' >> /repo/mocks/sublime.py
RUN echo '        pass' >> /repo/mocks/sublime.py
RUN echo '    def run_command(self, cmd):' >> /repo/mocks/sublime.py
RUN echo '        pass' >> /repo/mocks/sublime.py
RUN echo '' >> /repo/mocks/sublime.py
RUN echo 'LITERAL = 1' >> /repo/mocks/sublime.py
RUN echo 'ENCODED_POSITION = 2' >> /repo/mocks/sublime.py
RUN echo '' >> /repo/mocks/sublime.py
RUN echo 'def active_window():' >> /repo/mocks/sublime.py
RUN echo '    return Window()' >> /repo/mocks/sublime.py
RUN echo '' >> /repo/mocks/sublime.py
RUN echo 'def load_settings(filename):' >> /repo/mocks/sublime.py
RUN echo '    class Settings:' >> /repo/mocks/sublime.py
RUN echo '        def set(self, key, value):' >> /repo/mocks/sublime.py
RUN echo '            pass' >> /repo/mocks/sublime.py
RUN echo '        def get(self, key, default=None):' >> /repo/mocks/sublime.py
RUN echo '            return default' >> /repo/mocks/sublime.py
RUN echo '    return Settings()' >> /repo/mocks/sublime.py
RUN echo '' >> /repo/mocks/sublime.py
RUN echo 'def run_command(cmd):' >> /repo/mocks/sublime.py
RUN echo '    pass' >> /repo/mocks/sublime.py
ENV PYTHONPATH=/repo/mocks:/repo:$PYTHONPATH
RUN python -c "import sublime; import unittesting; print('Mock imports work')"
ENV PYTHONPATH=/repo/mocks:/repo:$PYTHONPATH
RUN grep -rh "sublime\." /repo/lint/*.py /repo/lint/**/*.py 2>/dev/null | grep -oE "sublime\.[a-zA-Z_]+" | sort -u | head -30
RUN echo '' >> /repo/mocks/sublime.py
RUN echo 'def platform():' >> /repo/mocks/sublime.py
RUN echo '    return "linux"' >> /repo/mocks/sublime.py
RUN echo '' >> /repo/mocks/sublime.py
RUN echo 'def packages_path():' >> /repo/mocks/sublime.py
RUN echo '    return "/repo"' >> /repo/mocks/sublime.py
RUN echo '' >> /repo/mocks/sublime.py
RUN echo 'def windows():' >> /repo/mocks/sublime.py
RUN echo '    return [Window()]' >> /repo/mocks/sublime.py
RUN echo '' >> /repo/mocks/sublime.py
RUN echo 'def set_timeout(func, delay=0):' >> /repo/mocks/sublime.py
RUN echo '    func()' >> /repo/mocks/sublime.py
RUN echo '' >> /repo/mocks/sublime.py
RUN echo 'def set_timeout_async(func, delay=0):' >> /repo/mocks/sublime.py
RUN echo '    func()' >> /repo/mocks/sublime.py
RUN echo '' >> /repo/mocks/sublime.py
RUN echo 'def status_message(msg):' >> /repo/mocks/sublime.py
RUN echo '    pass' >> /repo/mocks/sublime.py
RUN echo '' >> /repo/mocks/sublime.py
RUN echo 'def expand_variables(text, variables):' >> /repo/mocks/sublime.py
RUN echo '    return text' >> /repo/mocks/sublime.py
RUN echo '' >> /repo/mocks/sublime.py
RUN echo 'def decode_value(text):' >> /repo/mocks/sublime.py
RUN echo '    import json' >> /repo/mocks/sublime.py
RUN echo '    return json.loads(text)' >> /repo/mocks/sublime.py
RUN echo '' >> /repo/mocks/sublime.py
RUN echo 'def find_resources(pattern):' >> /repo/mocks/sublime.py
RUN echo '    return []' >> /repo/mocks/sublime.py
RUN echo '' >> /repo/mocks/sublime.py
RUN echo 'def load_resource(path):' >> /repo/mocks/sublime.py
RUN echo '    return ""' >> /repo/mocks/sublime.py
RUN echo '' >> /repo/mocks/sublime.py
RUN echo 'class Edit:' >> /repo/mocks/sublime.py
RUN echo '    pass' >> /repo/mocks/sublime.py
RUN echo '' >> /repo/mocks/sublime.py
RUN echo 'class BufferId:' >> /repo/mocks/sublime.py
RUN echo '    pass' >> /repo/mocks/sublime.py
RUN echo '' >> /repo/mocks/sublime.py
RUN echo 'class WindowId:' >> /repo/mocks/sublime.py
RUN echo '    pass' >> /repo/mocks/sublime.py
RUN pip show jsonschema
RUN pip install -q jsonschema<4.0.0
RUN pip show jsonschema
ENV PYTHONPATH=/repo/mocks:/repo:$PYTHONPATH
RUN echo '' >> /repo/mocks/sublime.py
RUN echo 'DRAW_SOLID_UNDERLINE = 1' >> /repo/mocks/sublime.py
RUN echo 'DRAW_NO_FILL = 2' >> /repo/mocks/sublime.py
RUN echo 'DRAW_EMPTY = 4' >> /repo/mocks/sublime.py
RUN echo 'HIDDEN = 8' >> /repo/mocks/sublime.py
RUN echo 'PERSISTENT = 16' >> /repo/mocks/sublime.py
RUN echo 'SCOPE_WORD = 32' >> /repo/mocks/sublime.py
RUN grep -rh "sublime_plugin\." /repo/*.py /repo/lint/*.py /repo/tests/*.py 2>/dev/null | grep -oE "sublime_plugin\.[a-zA-Z_]+" | sort -u
RUN echo 'class ApplicationCommand:' > /repo/mocks/sublime_plugin.py
RUN echo '    pass' >> /repo/mocks/sublime_plugin.py
RUN echo '' >> /repo/mocks/sublime_plugin.py
RUN echo 'class EventListener:' >> /repo/mocks/sublime_plugin.py
RUN echo '    pass' >> /repo/mocks/sublime_plugin.py
RUN echo '' >> /repo/mocks/sublime_plugin.py
RUN echo 'class TextCommand:' >> /repo/mocks/sublime_plugin.py
RUN echo '    pass' >> /repo/mocks/sublime_plugin.py
RUN echo '' >> /repo/mocks/sublime_plugin.py
RUN echo 'class WindowCommand:' >> /repo/mocks/sublime_plugin.py
RUN echo '    pass' >> /repo/mocks/sublime_plugin.py
RUN echo '' >> /repo/mocks/sublime_plugin.py
RUN echo 'def reload_plugin(name):' >> /repo/mocks/sublime_plugin.py
RUN echo '    pass' >> /repo/mocks/sublime_plugin.py
RUN echo '' >> /repo/mocks/sublime_plugin.py
RUN echo 'def unload_module(module):' >> /repo/mocks/sublime_plugin.py
RUN echo '    pass' >> /repo/mocks/sublime_plugin.py
ENV PYTHONPATH=/repo/mocks:/repo:$PYTHONPATH
RUN echo 'DRAW_NO_OUTLINE = 64' >> /repo/mocks/sublime.py
RUN echo 'DRAW_EMPTY_AS_OVERWRITE = 128' >> /repo/mocks/sublime.py
RUN mkdir -p /usr/local/lib/python3.10/site-packages/jsonschema/tests
RUN echo 'from io import StringIO' > /usr/local/lib/python3.10/site-packages/jsonschema/compat.py
RUN echo 'import unittest' >> /usr/local/lib/python3.10/site-packages/jsonschema/compat.py
RUN echo 'try:' >> /usr/local/lib/python3.10/site-packages/jsonschema/compat.py
RUN echo '    from collections.abc import Mapping, MutableMapping' >> /usr/local/lib/python3.10/site-packages/jsonschema/compat.py
RUN echo 'except ImportError:' >> /usr/local/lib/python3.10/site-packages/jsonschema/compat.py
RUN echo '    from collections import Mapping, MutableMapping' >> /usr/local/lib/python3.10/site-packages/jsonschema/compat.py
RUN echo 'import unittest' > /usr/local/lib/python3.10/site-packages/jsonschema/tests/__init__.py
RUN echo 'try:' >> /usr/local/lib/python3.10/site-packages/jsonschema/tests/compat.py
RUN echo '    from unittest import mock' >> /usr/local/lib/python3.10/site-packages/jsonschema/tests/compat.py
RUN echo 'except ImportError:' >> /usr/local/lib/python3.10/site-packages/jsonschema/tests/compat.py
RUN echo '    import mock' >> /usr/local/lib/python3.10/site-packages/jsonschema/tests/compat.py
RUN echo 'import unittest' >> /usr/local/lib/python3.10/site-packages/jsonschema/tests/compat.py
ENV PYTHONPATH=/repo/mocks:/repo:$PYTHONPATH
RUN echo 'str_types = (str,)' >> /usr/local/lib/python3.10/site-packages/jsonschema/compat.py
RUN echo 'from urllib.parse import urlsplit' >> /usr/local/lib/python3.10/site-packages/jsonschema/compat.py
ENV PYTHONPATH=/repo/mocks:/repo:$PYTHONPATH
RUN echo 'PY3 = True' >> /usr/local/lib/python3.10/site-packages/jsonschema/compat.py
RUN echo 'def iteritems(d): return d.items()' >> /usr/local/lib/python3.10/site-packages/jsonschema/compat.py
ENV PYTHONPATH=/repo/mocks:/repo:$PYTHONPATH
RUN echo 'int_types = (int,)' >> /usr/local/lib/python3.10/site-packages/jsonschema/compat.py
ENV PYTHONPATH=/repo/mocks:/repo:$PYTHONPATH
RUN echo 'from collections.abc import Sequence' >> /usr/local/lib/python3.10/site-packages/jsonschema/compat.py
ENV PYTHONPATH=/repo/mocks:/repo:$PYTHONPATH
RUN echo 'from functools import lru_cache' >> /usr/local/lib/python3.10/site-packages/jsonschema/compat.py
ENV PYTHONPATH=/repo/mocks:/repo:$PYTHONPATH
RUN echo 'from urllib.parse import unquote, urljoin, urlsplit' >> /usr/local/lib/python3.10/site-packages/jsonschema/compat.py
ENV PYTHONPATH=/repo/mocks:/repo:$PYTHONPATH
RUN echo 'from urllib.parse import urldefrag' >> /usr/local/lib/python3.10/site-packages/jsonschema/compat.py
ENV PYTHONPATH=/repo/mocks:/repo:$PYTHONPATH
RUN echo 'from urllib.request import urlopen' >> /usr/local/lib/python3.10/site-packages/jsonschema/compat.py
ENV PYTHONPATH=/repo/mocks:/repo:$PYTHONPATH
ENV PYTHONPATH=/repo/mocks:/repo:$PYTHONPATH
ENV PYTHONPATH=/repo/mocks:/repo:$PYTHONPATH
ENV PYTHONPATH=/repo/mocks:/repo:$PYTHONPATH
ENV PYTHONPATH=/repo/mocks:/repo:$PYTHONPATH
ENV PYTHONPATH=/repo/mocks:/repo:$PYTHONPATH
ENV PYTHONPATH=/repo/mocks:/repo:$PYTHONPATH
RUN rm -rf /repo/vendor/jsonschema/tests
ENV PYTHONPATH=/repo/mocks:/repo:$PYTHONPATH