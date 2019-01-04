FROM ubuntu:18.04

WORKDIR /app

# Add curl here
RUN apt-get -y update && apt-get -y install openjdk-8-jdk hfst python3 python3-pip git curl wget

# Install git-lfs repo
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash

# Install git-lfs
RUN apt-get -y install git-lfs

# Use git lfs for clone to make the process foolproof
RUN git lfs clone --recurse-submodules https://github.com/dlt-rilmta/e-magyar-tsv .
# RUN git checkout 1c618d89493cda9510adecc9fcb6811636988e4c

RUN pip3 install Cython
RUN pip3 install -r emmorphpy/requirements.txt
RUN pip3 install -r purepospy/requirements.txt
RUN pip3 install -r emdeppy/requirements.txt
RUN pip3 install -r HunTag3/requirements.txt

# Install locales. Any UTF-8 locale will do.
RUN apt-get -y install locales
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN make -C emtokenpy/ all

CMD ["python3", "./emtsv.py", "tok,morph,pos"]
