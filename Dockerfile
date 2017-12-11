FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    python3-setuptools \
  && rm -rf /var/lib/apt/lists/*


RUN pip3 install uwsgi

ADD * /home/

RUN pip3 install -r /home/requirements.txt

CMD ["uwsgi", "--ini", "/home/uwsgi.ini"]

EXPOSE 8000
#EXPOSE 443