# Use official Python image with the version you want
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy all your app files
COPY . .

# Set environment variables (optional, you can also set them on Fly)
# ENV OPENAI_API_KEY=yourkey ...

# Run your main bot script
CMD ["python", "main.py"]
