FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required by OpenCV
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libgl1 \
        libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# # Copy the requirements file and install dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install redis && \
    pip install numpy && \
    pip install Flask && \
    pip install gunicorn && \
    pip install Flask-Mail && \ 
    pip install itsdangerous && \
    pip install mock && \
    pip install opencv-python

# Copy the rest of the application code
COPY app.py .
COPY app_factory.py .
COPY utils/ utils/  
COPY templates/ templates/
COPY static/ static/

# Run the application
# CMD ["python", "app.py"]
CMD ["gunicorn", "-b", "$BIND_ADDR:8000", "app:app"]
