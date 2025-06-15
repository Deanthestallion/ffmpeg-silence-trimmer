# Use a slim Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

# Expose port (Render sets $PORT env)
EXPOSE 5000

# Start using Gunicorn (main is your .py file, app is the Flask object)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
