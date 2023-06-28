# Use the official Python 3.9.16 image as the base
FROM python:3.9.16

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose the required port
EXPOSE 8080

# Set the entrypoint command
CMD ["python", "main.py"]

