# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements first to utilize caching
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Download TextBlob corpora
RUN python -m textblob.download_corpora

# Make port 5000 available to the world outside this container. not necessry 
EXPOSE 5000

# Copy the current directory contents into the container at /app
COPY . /app

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "main.py"]


