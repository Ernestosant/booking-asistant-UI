# Use Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PORT=8050

# Expose port needed by Cloud Run
EXPOSE 8050

# Command to run the application
CMD ["streamlit", "run", "--server.port", "${PORT}", "--server.address", "0.0.0.0", "app.py"]
