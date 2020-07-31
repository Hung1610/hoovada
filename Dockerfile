FROM pypy:3

WORKDIR /

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# EXPOSE 

CMD [ "pypy3", "./manage.py" ]