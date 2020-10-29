###########
# BUILDER #
###########

# pull official base image
FROM pypy:3 as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# lint
RUN pip install --upgrade pip
RUN pip install flake8
COPY . /usr/src/app/
RUN flake8 --ignore=E501,F401 .

# install python dependencies
COPY ./app/requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

#########
# FINAL #
#########

FROM pypy:3

WORKDIR /opt

COPY ./app/requirements.txt /opt/

RUN apt-get update -y && apt-get install -y enchant && apt-get install -y libenchant-dev && apt-get install -y hunspell-vi

#RUN pip3 install --no-cache-dir -r requirements.txt
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

ENV TZ=Asia/Ho_Chi_Minh

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime 

RUN addgroup app

RUN useradd -g app -d /dev/null -s /usr/sbin/nologin app

COPY --chown=app:app . /opt/

# change to the app user
USER app

RUN chmod +x /opt/docker/app/entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["/opt/docker/app/entrypoint.sh"]