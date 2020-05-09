FROM python:3.8-alpine as builder

LABEL description="tm1602-exporter" maintainer="github@compuix.com"

COPY ./  /src/
WORKDIR /src

RUN python3 -mpip install -U pip setuptools wheel tox \
    && python3 -mpip wheel -w /wheel . \
    && tox

FROM python:3.8-alpine

COPY --from=builder /wheel/*.whl /wheel/

RUN python3 -mpip install -f /wheel --no-index tm1602_exporter \
    && rm -r /wheel

EXPOSE 9116

CMD [ "/usr/local/bin/tm1602_exporter" ]
