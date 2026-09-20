# --- Car (Raspberry Pi) connection -----------------------------------------
# Override any of these on the command line, e.g. `make deploy PICAR_HOST=1.2.3.4`
PICAR_HOST     ?= 192.168.86.30
PICAR_USER     ?= rpicar
PICAR_PATH     ?= /home/rpicar/SunFounder_PiCar-V
PICAR_SERVICES ?= picar

SSH  := ssh $(PICAR_USER)@$(PICAR_HOST)
SYNC := rsync -az --human-readable --exclude-from=.deployignore ./ \
	$(PICAR_USER)@$(PICAR_HOST):$(PICAR_PATH)/

.PHONY: relay relay-local relay-mock deploy deploy-dry restart logs car-status

# --- Relay server (runs on this machine) ------------------------------------
relay:
	cd relay && source .venv/bin/activate && RELAY_PICAR_HOST=100.74.200.59 uvicorn relay.main:app --host 0.0.0.0 --port 8080 --reload

# Same, but against the car's LAN address (no Tailscale needed).
relay-local:
	cd relay && source .venv/bin/activate && RELAY_PICAR_HOST=$(PICAR_HOST) uvicorn relay.main:app --host 0.0.0.0 --port 8080 --reload

relay-mock:
	cd relay && source .venv/bin/activate && RELAY_MOCK_MODE=true uvicorn relay.main:app --host 0.0.0.0 --port 8080 --reload

# --- Deploying to the car ----------------------------------------------------
# Show what would be copied, without touching the car.
deploy-dry:
	$(SYNC) --dry-run --itemize-changes

# Copy the working tree to the car and restart the service.
# Does not delete remote files; .venv, .env and db.sqlite3 on the Pi are left alone.
deploy:
	$(SYNC)
	$(SSH) 'sudo systemctl restart $(PICAR_SERVICES)'
	@echo "Deployed to $(PICAR_USER)@$(PICAR_HOST):$(PICAR_PATH) and restarted: $(PICAR_SERVICES)"

restart:
	$(SSH) 'sudo systemctl restart $(PICAR_SERVICES)'

logs:
	$(SSH) 'journalctl -u $(PICAR_SERVICES) -n 80 --no-pager'

car-status:
	$(SSH) 'systemctl status $(PICAR_SERVICES) --no-pager -l | head -20'
