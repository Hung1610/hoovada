FROM pypy:3

WORKDIR /opt

COPY ./scheduled_jobs/requirements.txt /opt/

RUN apt-get update -y && apt-get install -y python3-dev

RUN pip3 install -r requirements.txt --ignore-installed

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime 

RUN addgroup app && groupmod -g 1000 app

RUN useradd -ms /usr/sbin/nologin app -g app

RUN usermod -u 1000 app

COPY --chown=app:app . /opt/

USER app

RUN chmod +x /opt/docker/scheduled_jobs/entrypoint.sh

ENTRYPOINT ["/opt/docker/scheduled_jobs/entrypoint.sh"]