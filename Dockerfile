
# FROM python:3.9
FROM python:3.9-slim


WORKDIR /app

# Copy the project files to the container
COPY . /app

# COPY Desktop/erp_env/app/deps
# COPY /Desktop/erp_env/lib/python3.8/site-packages/ /app/
# COPY /home/kiet/Desktop/erp_env/ /app/
# RUN sed -i 's/deb.debian.org/mirrors.ubuntu.com/g' /etc/apt/sources.list
# RUN apt-get update

# Install rsync (if not already installed in the base image)
# RUN apt-get update

# Use rsync to copy packages from erp_env to the container
# RUN rsync -av --exclude='*.pyc' /path/to/erp_env/lib/python3.8/site-packages/ /app/

# Install dependencies
RUN pip install -r requirement.txt

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Expose the Django development server port
EXPOSE 8000
# HOST=0.0.0.0 
# DANGEROUSLY_DISABLE_HOST_CHECK=True

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
