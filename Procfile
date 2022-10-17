release: yes "yes" | python manage.py migrate
web: uwsgi --http-socket=:$PORT --master --workers=2 --threads=8 --die-on-term --wsgi-file=scoresnow/wsgi.py  --static-map /media/=/app/scoresnow/media/ --offload-threads 1
