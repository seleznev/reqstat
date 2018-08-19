FROM debian:stretch

RUN set +e; \
    apt-get update; \
    apt-get install -y python3-yaml python3-prometheus-client

COPY reqstat /usr/local/lib/python3.5/dist-packages/reqstat
COPY bin/reqstatd /usr/local/bin/reqstatd
COPY config/reqstat.yml /etc/reqstat/reqstat.yml
RUN sed -i 's/ip: 127.0.0.1/ip: 0.0.0.0/' /etc/reqstat/reqstat.yml

EXPOSE 2671
EXPOSE 9071

CMD ["/usr/local/bin/reqstatd"]
