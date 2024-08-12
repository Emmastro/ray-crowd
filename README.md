# Reverse Proxy Deployment Guide

This guide provides detailed instructions for deploying the reverse proxy that enhances the Ray cluster. The reverse proxy is essential for managing client requests, implementing additional features like authentication, project management, and data filtering.

1. Set Up the Virtual Environment and Install Dependencies

Begin by setting up a Python virtual environment and installing the required dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
This step ensures an isolated environment for the application and installs all necessary packages listed in the requirements.txt file.


2. Database Management

Before running the application, initialize and migrate the database:

```bash
make db-init   # Initialize the database
make db-migrate  # Apply migrations
make db-upgrade  # Upgrade the database schema
```

3. Run the Reverse Proxy with Gunicorn

For production deployment, it is recommended to run the Flask application using Gunicorn with Uvicorn workers. This setup enhances performance and adds support for HTTP/2:

```bash
FLASK_APP=run.py FLASK_ENV=production venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:5000 run:app
```

