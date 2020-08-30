FROM pypy:3

WORKDIR /opt

COPY ./app/requirements.txt /opt/

RUN apt-get update -y && apt-get install -y enchant && apt-get install -y libenchant-dev && apt-get install -y hunspell-vi

RUN pip3 install --no-cache-dir -r requirements.txt

RUN addgroup gunicorn

RUN useradd -g gunicorn -d /dev/null -s /usr/sbin/nologin gunicorn 

COPY --chown=gunicorn:gunicorn . /opt/

USER gunicorn

EXPOSE 5000

ENTRYPOINT ["/opt/docker/app/entrypoint.sh"]