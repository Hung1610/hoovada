FROM pypy:3

WORKDIR /

COPY ./app/requirements.txt /

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ARG GIT_COMMIT=unspecified

LABEL git_commit=$GIT_COMMIT

RUN echo $git_commit > /git-commit.txt

ENTRYPOINT ["entrypoint.sh"]