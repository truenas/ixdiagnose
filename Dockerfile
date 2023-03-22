FROM ghcr.io/truenas/middleware:master

RUN chmod +x /usr/bin/apt*
RUN apt update
RUN apt install -y python3-pip

ENV PYTHONUNBUFFERED 1

ENV WORK_DIR /app
RUN mkdir -p ${WORK_DIR}
WORKDIR ${WORK_DIR}

ADD . ${WORK_DIR}/
RUN pip install -r requirements.txt
RUN pip install -U .
