FROM pypy:3

WORKDIR /opt

COPY ./app/requirements.txt /opt/

RUN apt-get update -y && apt-get install -y python-dev python3-dev libevent-dev enchant libmemcached-dev zlib1g-dev libenchant-dev hunspell-vi

RUN pip3 install --no-cache-dir -r requirements.txt --ignore-installed

ENV TZ=Asia/Ho_Chi_Minh

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime 

COPY . /opt/

RUN chmod +x /opt/docker/app_dramatiq/entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["/opt/docker/app_dramatiq/entrypoint.sh"]