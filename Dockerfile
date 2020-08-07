FROM pypy:3

WORKDIR /

COPY ./app/requirements.txt /

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG GIT_COMMIT=unspecified

LABEL git_commit=$GIT_COMMIT

RUN echo $git_commit > /git-commit.txt

CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]