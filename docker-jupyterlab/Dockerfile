FROM python:3

# Update package list and install dependent system libraries
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx

# Copy requirements.txt into container
COPY requirements.txt /tmp/requirements.txt

# Installing Python Libraries
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

# Working Directory Settings
WORKDIR /work
