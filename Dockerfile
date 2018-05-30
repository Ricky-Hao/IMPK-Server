FROM python:alpine
LABEL maintainer="Ricky Hao <a959695@live.com>"

VOLUME /server

COPY requirements.txt /root/requirements.txt
RUN apk add --no-cache --virtual .build_deps build-base python3-dev libffi-dev &&\
    apk add --no-cache openssl-dev &&\
    pip install -r /root/requirements.txt &&\
    apk del .build_deps

EXPOSE 30000

ENTRYPOINT ["python", "/server/run_server.py"]