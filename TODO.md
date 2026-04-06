## PiCar-V Remote Access — TODO

### Pi hardening
- [ ] Change default `pi` user password (or create a new user, delete `pi`)
- [ ] SSH: disable password auth, use key-only (`PasswordAuthentication no` in sshd_config)
- [ ] `sudo apt update && sudo apt full-upgrade`
- [ ] Enable `unattended-upgrades` for automatic security patches
- [ ] Set up `ufw` — default deny inbound, allow SSH + 8000 from localhost/tailnet only

### Fix the Django app
- [ ] `DEBUG = False` in settings.py
- [ ] Rotate `SECRET_KEY`, load from env var
- [ ] Set `ALLOWED_HOSTS` to your exact hostnames
- [ ] Rename `MIDDLEWARE_CLASSES` to `MIDDLEWARE`, drop `SessionAuthenticationMiddleware`
- [ ] Add `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SESSION_COOKIE_SAMESITE = 'Strict'`
- [ ] Fix `stream.py` `stop()` — remove `shell=True` + string interpolation (command injection)
- [ ] Bind Django to `127.0.0.1:8000` instead of `0.0.0.0:8000` in the `start` script
- [ ] Run `python manage.py check --deploy` and fix what it reports

### Tailscale (your personal access)
- [ ] Install Tailscale on the Pi (`curl -fsSL https://tailscale.com/install.sh | sh && sudo tailscale up`)
- [ ] Install Tailscale on your phone/laptop
- [ ] Enable MagicDNS in Tailscale admin
- [ ] Enable key expiry for the Pi node
- [ ] Set up ACLs — restrict which devices can reach the Pi
- [ ] Enable MFA on your Tailscale account

### Cloudflare Tunnel + Access (friends)
- [ ] Register a domain (or use an existing one) on Cloudflare
- [ ] Install `cloudflared` on the Pi
- [ ] Create a tunnel pointing to `localhost:8000`
- [ ] Route the MJPG stream (port 8080) through the **same tunnel** — don't leave it exposed separately
- [ ] Set up a Cloudflare Access application for the tunnel hostname
- [ ] Set auth policy: allow by email (add your friends' emails)
- [ ] Test: unauthenticated request should hit the Access login page, not the car

### Verify
- [ ] From your phone over Tailscale: car works
- [ ] From a friend's browser: Access login appears, then car works after auth
- [ ] From an anonymous browser: Access login appears, no way through without an allowed email
- [ ] MJPG stream is not reachable on any public port directly
