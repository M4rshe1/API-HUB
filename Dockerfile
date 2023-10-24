# Use the Python 3.7.4 Alpine base image
FROM ubuntu:latest

# Set the working directory to /app
WORKDIR /app

# Copy requirements.txt to the container at /app
COPY requirements.txt /app

# install newest python and pip
RUN apt update && apt install -y python3 python3-pip python3-venv

# Create venv
RUN python3 -m venv venv

# activate venv and install requirements
RUN . venv/bin/activate && pip3 install --trusted-host pypi.python.org -r requirements.txt

## install uwsgi
# RUN apt install -y uwsgi uwsgi-plugin-python3

# Copy the current directory contents into the container at /app
COPY . .

# Make port 6969 available to the world outside this container
EXPOSE 6969

# Run app.py when the container launches
#CMD ["uwsgi", "--ini", "uwsgi.ini"]
CMD ["/bin/bash", "-c", "source venv/bin/activate && python3 app.py"]

