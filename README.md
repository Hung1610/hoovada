# **Hoovada-services**

This is the repo for APIs services of project hoovada.com

Project Structure
---

We follow this [code structure example](https://github.com/frol/flask-restplus-server-example) with the following components:

- __app__
    
    This is the main component of the project, it consists of all main sub-modules of the project. 
    - extensions
    - modules
        - common
    - settings
    - templates
    - utils
    - apis.py
    - app.py
    - __requirements.txt__
- __deploy__
- __docs__
- __flask_restx_patched__
- __migrations__
- __sql__
- __tasks__
- __tests__
- __README.md__
- __manage.py__
- __.gitignore__
- __.pylintrc__


Development environment
---

- For Linux distribution, you might need to install dependencies
```
$ sudo apt install unixodbc-dev
$ sudo apt-get install python3-dev
```

- We use pypy3.6 running on conda environment

```
$ cd /tmp
$ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
$ sha256sum /tmp/Miniconda3-latest-Linux-x86_64.sh 
$ bash /tmp/Miniconda3-latest-Linux-x86_64.sh -b -p $HOME//usr/share/miniconda3
$ sudo ln -s /usr/share/miniconda3/bin/conda /usr/bin/

$ conda create --name pypy_env
$ conda env list
$ conda activate pypy_env

$ conda install -c conda-forge pypy3.6
$ ln -s $HOME/.conda/envs/pypy_env/bin/pypy3 $HOME/.conda/envs/pypy_env/bin/python

$ python -m ensurepip
$ python -m pip install --upgrade pip
$ pip3 install -r <path to project>/app/requirements.txt
```

- Run project:
```bash
python manage.py
```
