# Use the official lightweight Python image
# https://hub.docker.com/_/python
FROM python:3.10.9

# Allow statements and log messagees to immediatly appeat in the Knative logs
ENV PYTHONNUNBUFFERED True

#Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . /app

# Install production dependencies
RUN pip install -r requirements.txt
#RUN pip install ./dist/frontend-1.0.0-py3-none-any.whl
RUN flask --app frontend init-db
#RUN pip install uwsgi==2.0.19.1
#RUN pip install gunicorn

EXPOSE 5000

# Run the web services on container startup. Gere we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increas the number of worker.
# to be equal to the cores available.
# Timeout is set to 0 to diable the timeouts of the workers to allow Cloud Run to handle instance scalling.
#CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 frontend
#CMD "flask --app frontend init-db"
#CMD ["flask","--app","frontend","run"]
CMD gunicorn --bind=0.0.0.0:5000 --forwarded-allow-ips="*" "frontend:create_app()"