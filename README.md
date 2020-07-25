Hoovada-services Deployment Documentation
-----------------------------------

# 1. Project Structure
This project consists of the following components:
- __app__
    
    This is the main component of the project, it consists of all main sub-modules of the project. These modules are used to handle data, manage connections from client.
    - extensions
    - modules
        - common
    - settings
    - templates
    - utils
    - apis.py
    - app.py
- __deploy__
- __docs__
- __flask_restx_patched__
- __migrations__
- __sql__
- __statis__
- __tasks__
- __tests__
- __README.md__
- __manage.py__
- __requirements.txt__
- __.gitignore__

# 2. Deployment
## 2.1. Minimum Requirements (main libraries)
```yaml
- flask
- flask-restx
- flask-sqlalchemy
```


## 2.2. Deployment

- Install env

- Install required dependencies:

```bash
sudo apt install unixodbc-dev
sudo apt-get install python3-dev
pip install -r requirements.txt
```
- Run project:
```bash
python manage.py
```

