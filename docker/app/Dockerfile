FROM pypy:3

WORKDIR /opt

COPY ./app/requirements.txt /opt/

RUN apt-get update -y && apt-get install -y python-dev python3-dev libevent-dev enchant libmemcached-dev zlib1g-dev libenchant-dev aspell

RUN pip3 install --no-cache-dir -r requirements.txt --ignore-installed 

ENV TZ=Asia/Ho_Chi_Minh

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime 

RUN addgroup app && groupmod -g 1000 app

RUN useradd -ms /usr/sbin/nologin app -g app

RUN usermod -u 1000 app

COPY --chown=app:app . /opt/

WORKDIR /opt/aspell6-vi-0.01.1-1

RUN ./configure

RUN make

RUN make install

WORKDIR /opt

USER app

RUN chmod +x /opt/docker/app/entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["/opt/docker/app/entrypoint.sh"]