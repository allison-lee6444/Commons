run-server:
	cd server;\
	uvicorn main:app --host 127.0.0.1 --port 8060
run-uni-server:
	cd university_server;\
	uvicorn server:app --host 127.0.0.1 --port 8008
test:
	python -m pytest -vv