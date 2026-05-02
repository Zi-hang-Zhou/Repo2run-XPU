FROM python:3.10
WORKDIR /
COPY code_edit.py /code_edit.py
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pytest pytest-xdist
RUN pip install pipdeptree
RUN git clone https://github.com/google-deepmind/acme.git
RUN mkdir /repo
RUN git config --global --add safe.directory /repo
RUN cp -r /acme/. /repo && rm -rf /acme/
RUN rm -rf /acme
RUN reset_environment
RUN cd /repo && pip install -e . -q
RUN cd /repo && pip install jax==0.4.17 jaxlib==0.4.17 dm-haiku==0.0.10 flax==0.7.0 optax==0.1.7 chex==0.1.7 rlax==0.1.7 -q
RUN cd /repo && pip install tensorflow==2.8.0 tensorflow-probability==0.15.0 tensorflow_datasets==4.9.9 dm-sonnet==2.0.2 trfl==1.2.0 -q
RUN apt-get update -qq
RUN apt-get install cmake -y -qq
RUN pip install pytest-xdist==3.8.0 pytype==2024.10.11 atari-py==0.2.9 bsuite==0.3.5 dm-control==1.0.38 gym==0.25.0 pygame==2.6.1 rlds==0.1.8 -q
RUN pip install dm-reverb==0.7.2 dm-launchpad==0.5.2 -q
RUN pip install tensorflow==2.11.0 tensorflow-probability==0.19.0 -q
RUN pip install protobuf==3.20.3 -q
RUN pip install tensorflow==2.12.0 tensorflow-probability==0.20.0 protobuf==3.20.3 -q
RUN pip install numpy==1.24.0 jax==0.4.17 jaxlib==0.4.17 flax==0.7.0 optax==0.1.7 chex==0.1.7 rlax==0.1.7 dm-haiku==0.0.10 -q
RUN pip install tensorflow==2.15.0 tensorflow-probability==0.23.0 -q
RUN pip uninstall dm-launchpad dm-reverb courier -y -q
RUN pip install dm-launchpad==0.5.2 dm-reverb==0.7.2 -q
RUN pip show dm-launchpad | grep -i requires
RUN pip index versions dm-launchpad 2>/dev/null | head -10
RUN pip install tensorflow==2.8.0 tensorflow-probability==0.15.0 protobuf==3.19.6 -q
RUN pip install dm-launchpad==0.5.2 dm-reverb==0.7.2 -q
RUN pip show scipy | grep -i version
RUN pip install scipy==1.11.4 -q