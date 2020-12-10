FROM pypy:3

WORKDIR /opt

COPY ./scheduled_jobs/requirements.txt /opt/

RUN apt-get update -y && apt-get install -y python3-dev

RUN pip3 install -r requirements.txt --ignore-installed

COPY . /opt/

RUN chmod +x /opt/docker/scheduled_jobs/entrypoint.sh

ENTRYPOINT ["/opt/docker/scheduled_jobs/entrypoint.sh"]