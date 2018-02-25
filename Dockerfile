FROM alpine:3.7
COPY ./requirements.txt /tmp
COPY ./application/ /application/
COPY ./entrypoint.sh /
RUN apk update && \
      /sbin/apk add python py2-pip build-base python-dev linux-headers && \
      /usr/bin/pip install -r /tmp/requirements.txt && \
      /sbin/apk del build-base python-dev linux-headers && \
      /bin/chmod +x /application/scripts/* && \
      /bin/chmod +x /entrypoint.sh && \
      /bin/rm -rf /var/cache/apk/* && \
      /bin/rm -rf /tmp/*
EXPOSE 8080
STOPSIGNAL SIGINT
ENTRYPOINT ["/entrypoint.sh"]
