# Use the official Python image as a base image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install any system-level dependencies (if needed)
# For example, you can install system packages using apt-get

# Install pipenv (if not already installed)
RUN pip install pipenv

# Set environment variables to use Pipenv
ENV PIPENV_VENV_IN_PROJECT 1
ENV PIPENV_IGNORE_VIRTUALENVS 1

# Install project dependencies using Pipenv
RUN pipenv install --deploy --ignore-pipfile

# Expose the port that the Flask app will run on (usually 5000)
EXPOSE 5000

# Set the entry point for running the Flask app
CMD ["pipenv", "run", "python", "app.py"]

