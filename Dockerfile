# Use official Python runtime as a parent image
FROM python:3.13.1-slim
 
# Set the working directory in the container
WORKDIR /usr/src/app
 
# Copy the current directory contents into the container at /usr/src/app
COPY . .
 
# Install dependencies
RUN pip install --no-cache-dir -r req.txt
 
# Expose the port your app runs on
EXPOSE 5000
 
# Define the environment variable for Flask
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
 
# Command to run the application
CMD ["flask", "run"]