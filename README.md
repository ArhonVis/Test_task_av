## NEED
1) redis
2) postgresql
3) pip install -r requirements.txt

## start celery
[python_path] -m celery -A celery_tasks.celery worker --loglevel=info --pool=solo

## start web monitoring
[python_path] -m celery -A celery_tasks.celery flower --port=[port]


