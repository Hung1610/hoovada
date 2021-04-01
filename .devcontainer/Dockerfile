FROM pypy:3

WORKDIR /opt

ENV PYTHONUNBUFFERED 1

COPY ./app/requirements.txt /opt/

RUN apt-get update -y && apt-get install -y python-dev python3-dev libevent-dev enchant libmemcached-dev zlib1g-dev libenchant-dev aspell python3-venv

RUN pip3 install --no-cache-dir -r requirements.txt --ignore-installed

ENV TZ=Asia/Ho_Chi_Minh

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime

RUN addgroup app && groupmod -g 1000 app && useradd -ms /usr/sbin/nologin app -g app && usermod -u 1000 app

COPY --chown=app:app . /opt/

WORKDIR /opt/aspell6-vi-0.01.1-1

RUN ./configure && make && make install

WORKDIR /opt

USER app

ENTRYPOINT ["/opt/docker/app/entrypoint.sh"]
