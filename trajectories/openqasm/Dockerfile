FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/openqasm/openqasm.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /openqasm/. /repo && rm -rf /openqasm/
RUN rm -rf /openqasm
RUN ls -la /repo/*.py /repo/*.toml /repo/*.lock 2>/dev/null || echo "No py/toml/lock files found"
RUN find /repo -name "setup.py" -o -name "pyproject.toml" -o -name "poetry.lock" -o -name "requirements*.txt" 2>/dev/null | head -20
RUN cat /repo/.github/workflows/*.yml 2>/dev/null | head -100
RUN cat /repo/source/grammar/setup.cfg 2>/dev/null || echo "No setup.cfg in grammar"
RUN cd /repo/source/openqasm && pip install -q -e .[all]
RUN cd /repo/source/grammar && pip install -q -e .[all]
RUN apt-get update -qq
RUN apt-cache search openjdk | grep -E "openjdk-[0-9]+-jdk" | head -5
RUN apt-get install -y -qq openjdk-21-jdk-headless
RUN cat /repo/source/openqasm/tools/*.py 2>/dev/null | head -50
RUN cd /repo && mkdir -p .antlr_jars
RUN cd /repo && mkdir -p source/openqasm/openqasm3/_antlr
RUN cd /repo/source/grammar && for version in 4.7.2 4.8 4.9.2 4.10.1 4.11.1 4.12.0 4.13.0; do curl -sLO "https://www.antlr.org/download/antlr-${version}-complete.jar" -o "../.antlr_jars/antlr-${version}-complete.jar"; done
RUN cd /repo/source/grammar && mv /repo/source/grammar/*.jar /repo/.antlr_jars/ 2>/dev/null; ls -la /repo/.antlr_jars/
RUN cd /repo/source/grammar && for version_string in 4.7.2 4.8 4.9.2 4.10.1 4.11.1 4.12.0 4.13.0; do IFS=. read -ra version <<< "${version_string}"; out_dir="/repo/source/openqasm/openqasm3/_antlr/_${version[0]}_${version[1]}"; mkdir -p "$out_dir"; java -Xmx500M -jar "/repo/.antlr_jars/antlr-${version_string}-complete.jar" -o "$out_dir" -Dlanguage=Python3 -visitor qasm3Lexer.g4 qasm3Parser.g4; done
RUN cd /repo/source/grammar && java -Xmx500M -jar "/repo/.antlr_jars/antlr-4.13.0-complete.jar" -o "openqasm_reference_parser" -Dlanguage=Python3 -visitor qasm3Lexer.g4 qasm3Parser.g4