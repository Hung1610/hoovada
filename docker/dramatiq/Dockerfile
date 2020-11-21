FROM pypy:3

WORKDIR /opt

COPY ./app/requirements.txt /opt/

RUN apt-get update -y && apt-get install -y python-dev python3-dev libevent-dev enchant libmemcached-dev zlib1g-dev libenchant-dev hunspell-vi

RUN pip3 install --no-cache-dir -r requirements.txt --ignore-installed

ENV TZ=Asia/Ho_Chi_Minh

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime 

RUN addgroup app

RUN useradd -g app -d /dev/null -s /usr/sbin/nologin app

COPY --chown=app:app . /opt/

# change to the app user
USER app

RUN chmod +x /opt/docker/dramatiq/entrypoint-dramatiq.sh

EXPOSE 5002

ENTRYPOINT ["/opt/docker/dramatiq/entrypoint-dramatiq.sh"]