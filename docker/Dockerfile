FROM python:latest
LABEL maintainer="Ricky Hao <a959695@live.com>"

VOLUME /server

COPY requirements.txt /root/requirements.txt
RUN pip install -r /root/requirements.txt

EXPOSE 30000

ENTRYPOINT ["python", "/server/run_server.py"]