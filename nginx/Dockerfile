FROM nginxinc/nginx-unprivileged:1.20-alpine

COPY ./default.conf.tpl /etc/nginx/default.conf.tpl

ENV LISTEN_PORT=8000 \
    APP_HOST=app \
    APP_LISTEN=8000

USER root

RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf

VOLUME /vol/static

USER nginx

COPY ./run.sh /run.sh

RUN chmod +x /run.sh

CMD ["./run.sh"]
