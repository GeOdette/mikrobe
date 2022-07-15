FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:02ab-main

# RUN apt-get update
# RUN apt-get install -y curl

# Install mccoretx

# RUN git clone --recursive -b geno_kmer_count https://github.com/Mykrobe-tools/mccortex mccortex &&\
# cd mccortex &&\
# make

# change dir
# RUN cd ..

# build from source on a Linux container
# RUN curl -L https://github.com/Mykrobe-tools/mykrobe/archive/refs/tags/v0.11.0.tar.gz -o /root/mykrobe.tar.gz &&\
# tar -xvf /root/mykrobe.tar.gz &&\
# cd /root/mykrobe-0.11.0 &&\
# python3 -m pip install .

#Install conda
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
RUN apt-get update
RUN apt-get install -y wget && rm -rf /var/lib/apt/lists/*
RUN wget \
  https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
  && mkdir /root/.conda \
  && bash Miniconda3-latest-Linux-x86_64.sh -b \
  && rm -f Miniconda3-latest-Linux-x86_64.sh 

# Installing mykrobe. ACtivating conda environemtn does not work
# this does not work: SHELL ["/bin/bash", "-c"]
RUN conda config --add channels bioconda --add channels conda-forge
RUN conda install -c bioconda mykrobe &&\ 
  git clone --recursive -b geno_kmer_count https://github.com/Mykrobe-tools/mccortex mccortex &&\ 
  cd mccortex &&\
  make
# this does not work: echo "source activate snippy" > ~/.bashrc
RUN mykrobe panels update_metadata
RUN mykrobe panels update_species all

COPY wf /root/wf
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN python3 -m pip install --upgrade latch
RUN python3 -m pip install -U mongoengine
# RUN pip install --upgrade requests==2.20.1
WORKDIR /root
ENV LATCH_AUTHENTICATION_ENDPOINT https://nucleus.latch.bio
