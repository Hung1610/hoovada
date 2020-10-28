FROM pypy:3

WORKDIR /opt

COPY ./app/requirements.txt /opt/

RUN apt-get update -y && apt-get install -y enchant && apt-get install -y libenchant-dev && apt-get install -y hunspell-vi

RUN pip3 install --no-cache-dir -r requirements.txt

ENV TZ=Asia/Ho_Chi_Minh

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime 

ARG ENVIRONMENT

ENV ENVIRONMENT=$ENVIRONMENT

RUN addgroup app

RUN useradd -g app -d /dev/null -s /usr/sbin/nologin app

COPY --chown=app:app . /opt/

# change to the app user
USER app

RUN chmod +x /opt/docker/app/entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["/opt/docker/app/entrypoint.sh"]