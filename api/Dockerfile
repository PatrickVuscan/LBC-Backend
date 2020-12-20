# The "buster" flavor of the official docker Python image is based on Debian and includes common packages.
FROM python:3.8.5-buster

# Create the working directory.
RUN set -ex && mkdir /repo
WORKDIR /repo

ENV PORT 8080

COPY api/ ./api
COPY requirements.txt .
COPY authentication.py .

# Install Python dependencies.
RUN set -ex && pip3 install -r ./requirements.txt 

# Run the web server.
EXPOSE $PORT
ENV PYTHONPATH /repo
CMD python3 /repo/api/app.py
