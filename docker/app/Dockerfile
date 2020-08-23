FROM pypy:3

WORKDIR /opt

COPY ./app/requirements.txt /opt/

RUN pip3 install --no-cache-dir -r requirements.txt

RUN addgroup gunicorn

RUN useradd -g gunicorn -d /dev/null -s /usr/sbin/nologin gunicorn 

COPY --chown=gunicorn:gunicorn . /opt/

ARG GIT_COMMIT=unspecified

LABEL git_commit=$GIT_COMMIT

RUN echo $git_commit > /git-commit.txt

USER gunicorn

EXPOSE 5000

ENTRYPOINT ["/opt/docker/app/entrypoint.sh"]