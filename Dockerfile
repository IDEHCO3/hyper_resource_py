FROM mapnik-3.0.10-node-python:latest

RUN apt-get update && apt-get install -y libpq-dev libgdal-dev memcached

RUN mkdir /code

RUN pip install \
	bcrypt==3.1.3 \
	certifi==2017.7.27.1 \
	cffi==1.10.0 \
	chardet==3.0.4 \
	Django==1.11.1 \
	django-cors-headers==2.1.0 \
	django-filter==1.0.4 \
	django-simple-captcha==0.5.5 \
	djangorestframework==3.6.3 \
	djangorestframework-gis==0.11.2 \
	djangorestframework-jwt==1.10.0 \
	falcon==1.2.0 \
	html5lib==0.999999999 \
	idna==2.5 \
	Markdown==2.6.8 \
	Pillow==3.1.0 \ 
	psycopg2==2.7.1 \
	pycparser==2.18 \
	PyJWT==1.5.0 \
	python-mimeparse==1.6.0 \
	pytz==2017.2 \
	requests==2.18.3 \
	six==1.10.0 \
	urllib3==1.22 \
	webencodings==0.5.1 \
	mapnik \
    geobuf \
	uwsgi \
	python-memcached==1.59 \
	#django-redis

# VERSION 1.0.0
# docker run -d -p 2008:2000 -v /home/ggt/docker-data-volume/python/munic:/code --name munic hyper_resource_py:1.0.0 uwsgi --ini /code/uwsgi.ini

