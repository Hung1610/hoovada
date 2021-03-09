# **Hoovada-services**

APIs services of the project hoovada.com


Project Overview
---

- We follow this [structure example](https://github.com/frol/flask-restplus-server-example)
- Configuration file is at app/settings/config.py, we use environment variables to manage conf in production.

### Built with

- Language: pypy3.6
- Framework: Flask 
- Database: MySQL
- OpenAPI: [flask-restx](https://flask-restx.readthedocs.io/en/latest/)
- Front-end data format: [Json](https://pyjwt.readthedocs.io/en/latest/)
- DB migration: [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/); the library could not detect every changes, i.e. change of data type. If migration does not work, please put the required sql command into sql/
- ORM: [SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- Hashing: [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/en/latest/)
- MySQL client library: [PyMySQL](https://pypi.org/project/PyMySQL/)
- Wasabi client library: [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs.html)
- twilio client library: [twilio](https://pypi.org/project/twilio/)


Development instruction
---

- Testing: [staging](https://staging.hoovada.com) and [test](https://test.hoovada.com)
- Production: [hoovada.com](https://hoovada.com)

### Branch

- Please branch out from dev 

```bash
$ git clone https://gitlab.com/hoovada/hoovada-services.git
$ git checkout -b dev origin/dev
$ git checkout -b <your branch name> dev

// do your development

$ git add --all 
$ git commit -s -am "your message"

// You might also need to rebase from upstream remote branch before pushing
$ git rebase upstream/dev

// To push your branch
$ git push -u origin <your branch name>
```

- Then you can create merge-request (top left corner of gitlab UI) with the source branch is your branch and the target branch is dev branch.


#### Quick testing with docker

```bash
$ docker build -f ./docker/app/Dockerfile .
$ docker run <name of image>
```

#### Running API services on Linux

- To run API services on local

```bash
// For Linux distribution, you might need to install dependencies
$ apt-get update -y && apt-get install -y enchant && apt-get install -y libenchant-dev && apt-get install -y hunspell-vi

//  We use pypy3.6 running on production, you can follow these step to set up pypy3.6 on conda environment for Linux
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
$ pip3 install -r <path to project>/requirements.txt --ignore-installed

// Run APIs and socketIO on development environment

$ ./%HOME/.conda/envs/pypy_env/bin/python <path to project>/manage.py -m dev -p <port>
$ ./%HOME/.conda/envs/pypy_env/bin/python <path to project>/manage_socketio.py -m dev -p <port>
```

- If you face with mixed-content issues https vs http, change api = HTTPSApi() to api=Api() in app/apis.py.

- Setting up DB

```bash
$ mysql -u username -p hoovada < ./sql/before_migration.sql

CREATE USER IF NOT EXISTS <user>@'%' IDENTIFIED BY <password>;
GRANT ALL PRIVILEGES ON hoovada.* TO <user>@'%';
FLUSH PRIVILEGES;

// import data
$ mysql -u username -p hoovada < data.sql
```

#### Full set-up with docker-compose

- You can run both app and DB with docker-compose

```bash
// You need to build every time you update code
$ cd <path to project>
$ docker-compose build

// Docker-compose up will run 4 dockers: API, socketio, DB and adminer for DB UI, REMEMBER to re-build before re-rerunning this 
$ docker-compose up

// Some other useful commands
$ docker-compose ps
$ docker-compose logs <name of container>

// to completely wipe out the set-up
$ docker-compose stop
$ docker-compose rm
```

- Swagger:  http://localhost:5000/api/v1/openapi
- adminer:  http://localhost:80, user/password/db: dev/hoovada/hoovada

#### Generate new migration file
When you have changes for database. E.g: adding new table, you hate to do migration
https://flask-migrate.readthedocs.io/.
Firstly, access the backend environment to have flask-migrate already. Start db container and access it
```
docker-compose start backend
docker exec -it hoovada-services_backend_1 /bin/bash
```
In docker bash. Run:
```
flask db migrate -m "what you've changed in db"
```
check migrations/versions/ for the new file.
Next time when you run `flask db upgrade`, the migration is executing.


### Code quality

- Code style: Please follow  Pep8 coding style
- Third-party library:  Please add library + version into app/requirements.txt 
- Quote: Please use either ‘’ or “” but not both
- import statement:
	- Please use full path import
	- Recomend to import only necessary function not entire package, i.e. if you only need sqrt():
	```
		Recommended:  		from math import sqrt
		Not recommended:  	import math
	```

- Status code: Please use English only, i.e. in send_error and send_result.

- Exception - EAFP principle: use except/try instead of if/else, also if possible please use specific exceptions instead of generic exception.

- Plese use pylint before pushing code
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

