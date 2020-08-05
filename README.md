# **Hoovada-services**

APIs services of the project hoovada.com

Project Overview
---

- We follow this [structure example](https://github.com/frol/flask-restplus-server-example), the app directory is the main entry point

- The app/requirements.txt is where you should put your new third-party libraries

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

- Testing: run on 165.22.97.24, we expose OpenAPI on testing environment for frontend to integrate APIs.

- Development: developers' local desktop


### Development environment setup

- For Linux distribution, you might need to install dependencies

```bash
$ sudo apt install unixodbc-dev
$ sudo apt-get install python3-dev
```

- We use pypy3.6 running on production, you can follow these step to set up pypy3.6 on conda environment

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

### Branch

- Please branch out from dev 

```bash
$ git clone https://gitlab.com/hoovada/hoovada-services.git
$ git checkout -b dev origin/dev
$ git checkout <your branch name>

// do your development 
$ git add --all 
$ git commit -s -am "your message"

// You might also need to rebase from upstream remote branch before pushing
$ git rebase upstream/dev

// To push your branch
$ git push -u origin <your branch name>
```

### Run project on development environment

```bash
$ ./%HOME/.conda/envs/pypy_env/bin/python <path to project>/manage.py -m dev -p <port>
```

### Test on testing environment

- You can log in to testing environment at 165.22.97.24, and run your own branch

```bash
$ cd /home/dev/hoovada-services

// If the code is running in dev branch, you should stop it first
$ sudo systemctl stop hoovada
$ git checkout -b <your branch name> origin/<your branch name>
$ git fetch && git pull
$ sudo systemctl start hoovada

// you can see the stderr and stdout with
$ sudo journalctl -u hoovada -f
// Now you should see swagger of your branch at 165.22.97.24:<port>

// After finish testing your branch, you should revert back to dev branch
$ cd /home/dev/hoovada-services
$ git checkout dev
$ sudo systemctl restart hoovada
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

