start:
	python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt || pip install flask flask-mysqldb flask-cors && python3 server.py