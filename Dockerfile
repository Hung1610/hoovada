FROM pypy:3

WORKDIR /

COPY ./app/requirements.txt /

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# EXPOSE 

CMD [ "pypy3", "./manage.py" ]