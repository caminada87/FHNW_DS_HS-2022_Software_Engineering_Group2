# Use the official lightweight Python image
# https://hub.docker.com/_/python
FROM python:3

# Allow statements and log messagees to immediatly appeat in the Knative logs
ENV PYTHONNUNBUFFERED True

#Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies
RUN pip install -r requirements.txt
RUN pip install gunicorn

# Run the web services on container startup. Gere we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increas the number of worker.
# to be equal to the cores available.
# Timeout is set to 0 to diable the timeouts of the workers to allow Cloud Run to handle instance scalling.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 flask_hello:app