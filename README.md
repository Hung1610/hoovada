# **Hoovada-services**

APIs services of the project hoovada.com

Project Structure
---

We follow this [structure example](https://github.com/frol/flask-restplus-server-example), the app directory is the main entry point

- __app__
    - extensions
    - modules
        - common
        - auth
        - file_upload
        - messaging
        - q_a
            - answer
            - comment
            - favorite
            - question
            - report
            - share
            - timeline
            - voting
        - search
        - system
            - feedback
            - history
            - notification
            - request_log
            - version
        - topic
            - question_topic
            - user_topic
        - user
            - follow
            - mail_address
            - permission
            - reputation
            - user_permission
    - settings
    - templates
    - utils
    - apis.py
    - app.py
    - requirements.txt (please put all your third-party library here)


### Built with

- Language: pypy3.6
- Framework: Flask 
- Rest APIs and OpenAPI: [flask-restx](https://flask-restx.readthedocs.io/en/latest/)
- Front-end data format: Json with flask_restx.marshal
- DB migration: [alembic](https://pypi.org/project/alembic/)
- ORM: [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- MySQL client library: [PyMySQL](https://pypi.org/project/PyMySQL/)
- Wasabi storage client library: [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs.html)
- twilio client library; [twilio](https://pypi.org/project/twilio/)


### Services

- Database: MySQL
- Storage provider: wasabi
- Email delivery service: sendgrid
- SMS service: twilio
- SSL Certificate: Letsencrypt
- Server provider: digital ocean
- Hostname provider: namecheap

### Future consideration

- Framework: [Quart](https://pypi.org/project/Quart/)
- OpenAPI : [Quart-OpenAPI](https://github.com/factset/quart-openapi/)


Development instruction
---

### Environment setup

- For Linux distribution, you might need to install dependencies

```bash
$ sudo apt install unixodbc-dev
$ sudo apt-get install python3-dev
```

- We use pypy3.6 running for production, so you can follow these step to set up pypy3.6 on conda environment

```bash
$ cd /tmp
$ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
$ sha256sum /tmp/Miniconda3-latest-Linux-x86_64.sh 
$ bash /tmp/Miniconda3-latest-Linux-x86_64.sh -b -p /usr/share/miniconda3
$ sudo ln -s /usr/share/miniconda3/bin/conda /usr/bin/

$ conda create --name pypy_env
$ conda env list
$ conda activate pypy_env

$ conda install -c conda-forge pypy3.6
$ ln -s $HOME/.conda/envs/pypy_env/bin/pypy3 $HOME/.conda/envs/pypy_env/bin/python

$ python -m ensurepip
$ python -m pip install --upgrade pip
$ pip3 install -r <path to project>/requirements.txt
```

- Run project:

```bash
$ HOME/.conda/envs/pypy_env/bin/python <path to project>/manage.py
```

### Branch

- Please branch out from dev 

```bash
$ git clone https://gitlab.com/hoovada/hoovada-services.git
$ git checkout -b dev origin/dev
$ git checkout <your branch name>
// do your development 
$ git add --all 
$ git commit -s -am "your message"
$ git push -u origin <your branch name>
```

### Pylint

- We encourage developers to run Pylint before submitting code

```
$ pip3 install pylint
$ pylint <your files>
```

Versioning
---
We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://gitlab.com/hoovada/hoovada-services/-/tags). 

License
---
This project is licensed under a proprietary License - see the [LICENSE.md](LICENSE.md) file for details

