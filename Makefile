start up:
	python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt || pip install flask flask-mysqldb flask-cors && python3 server.py

init:
	python3 -m venv venv && . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
	@if [ ! -f .env ] && [ -f .env.example ]; then cp .env.example .env; fi