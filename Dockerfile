FROM tiangolo/uwsgi-nginx-flask:python3.8

WORKDIR /app
COPY . /app

RUN pip install Authlib==0.14.3
RUN pip install requests==2.22.0
RUN pip install Flask==1.1.1

EXPOSE 3000

# ENTRYPOINT uwsgi --ini /app/wsgi.ini
