# Use an official lightweight Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the necessary files
COPY ./main.py ./main.py
COPY ./Requirements.txt ./Requirements.txt
COPY ./player ./player
COPY ./board ./board

# Install required packages from the Requirements.txt
RUN pip install --no-cache-dir -r Requirements.txt

# Set environment variables
ENV FLASK_APP main.py
ENV FLASK_RUN_HOST 0.0.0.0

# Expose the port the app runs on
EXPOSE 5000

# Run the Flask application
CMD ["flask", "run"]
