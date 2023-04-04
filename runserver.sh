python manage.py collectstatic --no-input

python manage.py migrate

gunicorn --worker-tmp-dir /dev/shm djcrm.wsgi



username = doadmin
password = AVNS_SzxQc6pTXGbcDCp154j
host = db-postgresql-nyc1-29986-do-user-13887935-0.b.db.ondigitalocean.com
port = 25060
database = defaultdb
sslmode = require