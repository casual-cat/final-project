# Use the official Python 3.10 slim image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy only requirements.txt first for caching pip installs
COPY requirements.txt .

# Create the dbdata directory and set permissions
RUN mkdir -p /app/dbdata && chmod -R 777 /app/dbdata

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Explicitly copy the static directory (already included by `COPY .`, but for clarity)
COPY static /app/static

# Set environment variables for Flask
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Expose port 5000
EXPOSE 5000

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]