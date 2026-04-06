#!/bin/sh
set -e

# Start Tailscale daemon in userspace networking mode (no TUN needed in containers)
tailscaled --tun=userspace-networking --socks5-server=127.0.0.1:1055 --state=/var/lib/tailscale/tailscaled.state &

# Wait for tailscaled to be ready
sleep 2

# Authenticate with Tailscale (TS_AUTHKEY must be set as env var)
tailscale up --authkey="${TS_AUTHKEY}" --hostname=picar-relay

# Tell the relay to route traffic through the Tailscale SOCKS5 proxy
export RELAY_PROXY_URL="socks5://127.0.0.1:1055"

# Start the relay server
exec uvicorn relay.main:app --host 0.0.0.0 --port "${PORT:-8080}"
