FROM pypy:3

WORKDIR /opt

COPY ./app_socketio/requirements.txt /opt/

RUN pip3 install --no-cache-dir -r requirements.txt

RUN pip3 install --upgrade setuptools

ENV TZ=Asia/Ho_Chi_Minh

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime 

RUN addgroup gunicorn

RUN useradd -g gunicorn -d /dev/null -s /usr/sbin/nologin gunicorn 

COPY --chown=gunicorn:gunicorn . /opt/

USER gunicorn

RUN chmod +x /opt/docker/app_socketio/entrypoint.sh

EXPOSE 5001

ENTRYPOINT ["/opt/docker/app_socketio/entrypoint.sh"]