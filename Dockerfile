FROM python:2.7

ARG HTTP_PROXY
ARG HTTPS_PROXY

RUN pip install Flask requests
COPY view.py /
COPY entrypoint.sh /
COPY templates /templates

EXPOSE 5000

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
