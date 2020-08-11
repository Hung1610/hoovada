# **Hoovada-services**

APIs services of the project hoovada.com

Project Overview
---

- We follow this [structure example](https://github.com/frol/flask-restplus-server-example), the app directory is the main entry point.

- The app/requirements.txt is where you should put your new third-party libraries.

- Conf file is at app/settings/config.py, we use environment variables to manage conf in production. You can use the default values in config.py for your development.


### Built with

- Language: pypy3.6
- Framework: Flask 
- Database: MySQL (Percona Distribution)
- OpenAPI: [flask-restx](https://flask-restx.readthedocs.io/en/latest/)
- Front-end data format: [Json](https://pyjwt.readthedocs.io/en/latest/)
- DB migration: [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) and [alembic](https://pypi.org/project/alembic/)
- ORM: [SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- Hashing: [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/en/latest/)
- MySQL client library: [PyMySQL](https://pypi.org/project/PyMySQL/)
- Wasabi client library: [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs.html)
- twilio client library: [twilio](https://pypi.org/project/twilio/)


### Services

- Storage provider: wasabi
- Email delivery service: sendgrid
- SMS service: twilio
- Infrastructure provider: digital ocean
- Hostname provider: namecheap

### Future consideration

- Framework: [Quart](https://pypi.org/project/Quart/)
- OpenAPI : [Quart-OpenAPI](https://github.com/factset/quart-openapi/)


Development instruction
---

### Environments definition

- Production: the real environment where we deploy www.hoovada.com

- Staging: replicate production environment as much as possible

- Development: developers' local desktop

### Branch

- Please branch out from dev 

```bash
$ git clone https://gitlab.com/hoovada/hoovada-services.git
$ git checkout -b dev origin/dev
$ git checkout -b <your branch name>

// do your development 
$ git add --all 
$ git commit -s -am "your message"

// You might also need to rebase from upstream remote branch before pushing
$ git rebase upstream/dev

// To push your branch
$ git push -u origin <your branch name>
```

- Then you can create merge-request with the source branch being your branch and the target branch is dev branch


### Development environment setup

- For Linux distribution, you might need to install dependencies (optional)

```bash
$ sudo apt install unixodbc-dev
```

- We use pypy3.6 running on production, you can follow these step to set up pypy3.6 on conda environment for Linux

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
// For Macos, the location might be $HOME/miniconda/envs/pypy_env/bin/pypy3

$ python -m ensurepip
$ python -m pip install --upgrade pip
$ pip3 install -r <path to project>/requirements.txt
```

### Run project on development environment

```bash
$ ./%HOME/.conda/envs/pypy_env/bin/python <path to project>/manage.py -m dev -p <port>
```

- If you face with mixed-content issues https vs http, change api = MyApi() to api=Api() in app/apis.py for testing.

### Pylint

- We encourage developers to run Pylint before submitting code

```
$ pip3 install pylint
$ pylint <your files>
```

### Testing with docker image

- Please make sure that your branch can be built into docker image

```bash
$ docker build -t <name of image> .
$ docker image ls
$ docker run -p 80:5000 <name of image> 
```

- Browser to http://localhost:80/api/v1/doc to see your APIs.

- If you face with mixed-content issues https vs http, change api = MyApi() to api=Api() in app/apis.py for testing.


Versioning
---
We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://gitlab.com/hoovada/hoovada-services/-/tags). 


License
---
This project is licensed under a proprietary License - see the [LICENSE.md](LICENSE.md) file for details

