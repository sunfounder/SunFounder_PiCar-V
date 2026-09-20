.PHONY: relay relay-mock

relay:
	cd relay && source .venv/bin/activate && RELAY_PICAR_HOST=100.74.200.59 uvicorn relay.main:app --host 0.0.0.0 --port 8080 --reload

relay-mock:
	cd relay && source .venv/bin/activate && RELAY_MOCK_MODE=true uvicorn relay.main:app --host 0.0.0.0 --port 8080 --reload
