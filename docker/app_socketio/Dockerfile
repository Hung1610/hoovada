FROM pypy:3

WORKDIR /opt

COPY ./app_socketio/requirements.txt /opt/

RUN pip3 install --no-cache-dir -r requirements.txt

ENV TZ=Asia/Ho_Chi_Minh

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime 

RUN addgroup app && groupmod -g 1000 app

RUN adduser --ingroup app --home /dev/null --shell /usr/sbin/nologin app

RUN usermod -u 1000 app

COPY --chown=app:app . /opt/

USER app

RUN chmod +x /opt/docker/app_socketio/entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["/opt/docker/app_socketio/entrypoint.sh"]