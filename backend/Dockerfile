# build python3.7
FROM python:3.7

# maintainer jinchi.ca@outlook.com
MAINTAINER jiz148

# config python evironment variables
ENV PYTHONUNBUFFERED 1

# in container /var/www/html/, make workding directory
RUN mkdir -p /var/www/html/backend

# set working directory
WORKDIR /var/www/html/backend

# add current files to working directory
ADD . /var/www/html/backend

# pip install
RUN pip install -r requirements.txt

# remove \r becuase start.sh is writen in Windows
RUN sed -i 's/\r//' ./start.sh

# set chmod of start.sy
RUN chmod +x ./start.sh

# start service
ENTRYPOINT /bin/bash ./start.sh