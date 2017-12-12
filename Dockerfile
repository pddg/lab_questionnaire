FROM ubuntu:16.04


RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    python3-setuptools \
    git \
    locales \
  && rm -rf /var/lib/apt/lists/*

RUN locale-gen "en_US.UTF-8"
ENV LC_ALL "en_US.UTF-8"

RUN pip3 install uwsgi

ADD https://api.github.com/repos/erscl/lab_questionnaire/git/refs/heads/master version.json
RUN git clone https://github.com/erscl/lab_questionnaire.git /home
RUN pip3 install -r /home/requirements.txt

CMD ["/bin/bash", "/home/entrypoint.sh"]

EXPOSE 8000
#EXPOSE 443