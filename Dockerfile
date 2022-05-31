FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:02ab-main


ARG PKGS=" \
    build-essential \
    ca-certificates \
    git \
    gnupg \
    libbz2-dev \
    libcurl4-gnutls-dev \
    libssl-dev \
    liblzma-dev \
    python-is-python3 \
    python3-pip \
    tzdata \
    wget \
    zlib1g-dev \
    "

# mccortex
RUN apt-get install wget
RUN apt install sudo
RUN python -m pip install requests
RUN git clone --recursive -b geno_kmer_count https://github.com/Mykrobe-tools/mccortex mccortex
RUN cd mccortex
RUN make

# Clone mykrobe
RUN git clone https://github.com/Mykrobe-tools/mykrobe.git

RUN cd mykrobe
RUN pip3 install .
RUN mykrobe panels update_metadata
RUN mykrobe panels update_species all
# install mykrobe



COPY wf /root/wf
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN python3 -m pip install --upgrade latch
WORKDIR /root
ENV LATCH_AUTHENTICATION_ENDPOINT https://nucleus.latch.bio
