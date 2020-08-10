[loggers]
keys=root, gunicorn_error, gunicorn_access

[handlers]
keys=console

[formatters]
keys=json

[logger_root]
level=INFO
handlers=console

[logger_gunicorn.error]
level=DEBUG
handlers=console
propagate=0
qualname=gunicorn.error

[logger_gunicorn.access]
level=INFO
handlers=console
propagate=0
qualname=gunicorn.access

[handler_console]
class=StreamHandler
formatter=json
args=(sys.stdout, )

[formatter_json]
class=pythonjsonlogger.jsonlogger.JsonFormatter