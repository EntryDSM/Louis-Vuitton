FROM python:3.7-alpine

MAINTAINER JKS "jerion7474@gmail.com"

RUN apt-get update -y
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

ENV VAULT_TOKEN d13694738b11e72d71258e0449e0ad4c7c51be3e
ENV RUN_ENV production

COPY . .
WORKDIR .

RUN pip install -r requirements.txt

EXPOSE 3585

ENTRYPOINT ["python"]
CMD ["-m", "lv"]