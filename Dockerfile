FROM python:3.6-alpine

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD manage.py /code/
RUN mkdir /code/events
ADD events /code/events
RUN mkdir /code/eventmanager
ADD eventmanager /code/eventmanager
RUN mkdir /code/db
RUN python manage.py collectstatic --noinput
EXPOSE 80
ADD start.sh /code/
VOLUME ["/code/db",]
ENTRYPOINT /code/start.sh