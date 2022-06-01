FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:02ab-main

RUN apt-get update
RUN apt-get install -y curl

# build from source on a Linux container
RUN curl -L https://github.com/Mykrobe-tools/mykrobe/archive/refs/tags/v0.11.0.tar.gz -o /root/mykrobe.tar.gz &&\
  tar -xvf /root/mykrobe.tar.gz &&\
  cd /root/mykrobe-0.11.0 &&\
  python3 -m pip install .

RUN mykrobe panels update_metadata
RUN mykrobe panels update_species all

COPY wf /root/wf
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN python3 -m pip install --upgrade latch
WORKDIR /root
ENV LATCH_AUTHENTICATION_ENDPOINT https://nucleus.latch.bio
