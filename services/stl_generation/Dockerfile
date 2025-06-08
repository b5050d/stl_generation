FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# # Copy the requirements file and install dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install redis && \
    pip install numpy==2.2.5 && \
    pip install opencv-python==4.11.0.86 && \
    pip install matplotlib==3.10.3 && \
    pip install seaborn==0.13.2 && \
    pip install mapbox_earcut==1.0.3

# Copy the rest of the application code
COPY backend_link.py .
COPY ./modules .

# Run the application
CMD ["python", "backend_link.py"]
