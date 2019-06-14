FROM python:3.7-alpine

MAINTAINER JKS "jerion7474@gmail.com"

ENV VAULT_TOKEN $VAULT_TOKEN
ENV RUN_ENV production

COPY . .
WORKDIR .

RUN apk add --no-cache \
        gcc \
        make \
        musl-dev \
        libressl-dev \
        libffi-dev \
    && pip install -r requirements.txt \
    && apk del \
        gcc \
        make \
        musl-dev \
        libressl-dev \
        libffi-dev

EXPOSE 80

ENTRYPOINT ["python"]
CMD ["-m", "lv"]