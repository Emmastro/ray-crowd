include .env
# Variables
FLASK_APP = run.py
VENV = venv

# Setup virtual environment and install dependencies
setup:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

# Activate virtual environment
activate:
	@echo "Run 'source $(VENV)/bin/activate' to activate the virtual environment"

# Run the Flask application
run:
	FLASK_APP=$(FLASK_APP) FLASK_ENV=$(FLASK_ENV) $(VENV)/bin/flask run

# run guinicorn
run-gunicorn:
	FLASK_APP=$(FLASK_APP) FLASK_ENV=$(FLASK_ENV) $(VENV)/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:5000 run:app

run-asgi:
	hypercorn asgi:app -b 0.0.0.0:5000 --log-level info --access-log - --error-log - --reload
	# hypercorn asgi:app -b 0.0.0.0:5000 --log-config logging.conf --error-log -
	# hypercorn asgi:app -b 0.0.0.0:5000  --log-config logging.conf --error-log -
	

# Run tests
test:
	FLASK_APP=$(FLASK_APP) FLASK_ENV=testing $(VENV)/bin/python -m unittest discover tests

# Initialize the database
db-init:
	FLASK_APP=$(FLASK_APP) $(VENV)/bin/flask db init

# Migrate the database
db-migrate:
	FLASK_APP=$(FLASK_APP) $(VENV)/bin/flask db migrate -m "Initial migration."

# Upgrade the database
db-upgrade:
	FLASK_APP=$(FLASK_APP) $(VENV)/bin/flask db upgrade

db-delete:
	rm -rf migrations
	rm instance/app.db

# Run all database commands
db:
	make db-init
	make db-migrate
	make db-upgrade

# Clean the environment
clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf $(VENV)

# Install requirements
install:
	$(VENV)/bin/pip install -r requirements.txt

# Freeze requirements
freeze:
	$(VENV)/bin/pip freeze > requirements.lock.txt

# Help command
help:
	@echo "Makefile for Flask application"
	@echo "Usage:"
	@echo "  make setup          - Set up virtual environment and install dependencies"
	@echo "  make activate       - Show command to activate virtual environment"
	@echo "  make run            - Run the Flask application"
	@echo "  make test           - Run tests"
	@echo "  make db-init        - Initialize the database"
	@echo "  make db-migrate     - Migrate the database"
	@echo "  make db-upgrade     - Upgrade the database"
	@echo "  make db             - Run all database commands (init, migrate, upgrade)"
	@echo "  make clean          - Clean the environment"
	@echo "  make install        - Install requirements"
	@echo "  make freeze         - Freeze requirements to requirements.txt"
	@echo "  make help           - Show this help message"
 