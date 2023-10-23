# Use the Python 3.7.4 Alpine base image
FROM ubuntu:latest

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# install newest python and pip
RUN apt update && apt install -y python3 python3-pip python3-venv

# Create venv
RUN python3 -m venv venv

# activate venv and install requirements
RUN . venv/bin/activate && pip3 install --trusted-host pypi.python.org -r requirements.txt

# Make port 6969 available to the world outside this container
EXPOSE 6969

# Run app.py when the container launches
CMD ["python3", "app.py"]

