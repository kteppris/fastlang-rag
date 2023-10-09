FROM nvcr.io/nvidia/pytorch:23.08-py3

# Update the system and install C++ build dependencies.
RUN apt-get update -y && \
    apt-get install -y build-essential

# Sets the working directory in the Docker container
WORKDIR /app

# Copies the requirements file into the Docker container
COPY ./app/requirements.txt /app/

# Installs the Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copies the rest of the code into the Docker container
COPY ./app /app/

# Create data folder for models and docs
RUN mkdir /data

# Sets the command to run when the Docker container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
