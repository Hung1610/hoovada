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
    - __requirements.txt__

Development instruction
---

### Environment setup

- For Linux distribution, you might need to install dependencies
```
$ sudo apt install unixodbc-dev
$ sudo apt-get install python3-dev
```

- We use pypy3.6 running on conda environment for production (although you can use any python3 version for development)

```
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

```
$HOME/.conda/envs/pypy_env/bin/python <path to project>/manage.py
```

### Pylint

- We encourage developers to run Pylint before submitting code

```
$ pip3 install pylint
$ pylint <your files>
```

### logging




### DB migration



Built with
---

- Language: pypy3.6 on conda
- Backend Framework: Flask (moving to quartz in future)
- Frontend Framework: Angular
- Mobile Framework: React Native
- Data presentation: Json (moving to protobuf in future)
- Database: MySQL

### External services
- Storage provider: wasabi
- Email delivery service: sendgrid
- SMS service: twilio
- SSL Certificate: Letsencrypt
- Server provider: digital ocean
- Hostname provider: namecheap


Versioning
---
We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://gitlab.com/hoovada/hoovada-services/-/tags). 


Authors
---
* **hoovada.com team** 


License
---
This project is licensed under a proprietary License - see the [LICENSE.md](LICENSE.md) file for details

