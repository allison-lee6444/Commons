run-server:
	cd server;\
	uvicorn main:app --host 127.0.0.1 --port 8060 && python3 email/setup_gmail.py
test:
	python3 -m pytest