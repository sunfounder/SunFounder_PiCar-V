#!/bin/bash
set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$REPO_DIR/.venv"
ENV_FILE="$REPO_DIR/.env"

echo "=== PiCar-V Setup ==="
echo ""

# --- Step 1: Check system dependencies ---
echo "Checking system packages..."
missing=""
for pkg in python3-lgpio python3-smbus2; do
    if ! dpkg -s "$pkg" >/dev/null 2>&1; then
        missing="$missing $pkg"
    fi
done

if [ -n "$missing" ]; then
    echo "Missing system packages:$missing"
    echo "Installing..."
    sudo apt-get update -qq
    sudo apt-get install -y $missing
else
    echo "System packages OK."
fi

# Check I2C is enabled
if [ ! -e /dev/i2c-1 ]; then
    echo ""
    echo "WARNING: /dev/i2c-1 not found. I2C may not be enabled."
    echo "Run: sudo raspi-config nonint do_i2c 0 && sudo reboot"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# --- Step 2: Create venv ---
if [ -d "$VENV_DIR" ]; then
    echo ""
    echo "Virtual environment already exists at $VENV_DIR"
    read -p "Recreate it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$VENV_DIR"
        echo "Creating virtual environment..."
        python3 -m venv "$VENV_DIR" --system-site-packages
    fi
else
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR" --system-site-packages
fi

echo "Installing Python packages..."
"$VENV_DIR/bin/pip" install --quiet "django>=5.2,<6" gunicorn flask opencv-python-headless
echo "Python packages installed."

# --- Step 3: Create .env ---
echo ""
if [ -f "$ENV_FILE" ]; then
    echo ".env file already exists."
    read -p "Overwrite it? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Keeping existing .env"
        echo ""
        echo "=== Setup complete ==="
        echo "To run:  cd $REPO_DIR/remote_control && source $VENV_DIR/bin/activate && export \$(cat $ENV_FILE | xargs) && python3 manage.py runserver 127.0.0.1:8000"
        exit 0
    fi
fi

SECRET_KEY=$("$VENV_DIR/bin/python3" -c "import secrets; print(secrets.token_urlsafe(50))")

# Detect IP addresses for ALLOWED_HOSTS
LOCAL_IP=$(hostname -I 2>/dev/null | awk '{print $1}')
TAILSCALE_IP=$(tailscale ip -4 2>/dev/null || true)

echo "Detected local IP: ${LOCAL_IP:-none}"
if [ -n "$TAILSCALE_IP" ]; then
    echo "Detected Tailscale IP: $TAILSCALE_IP"
fi

DEFAULT_HOSTS="127.0.0.1,localhost"
[ -n "$LOCAL_IP" ] && DEFAULT_HOSTS="$DEFAULT_HOSTS,$LOCAL_IP"
[ -n "$TAILSCALE_IP" ] && DEFAULT_HOSTS="$DEFAULT_HOSTS,$TAILSCALE_IP"

echo ""
echo "ALLOWED_HOSTS controls which hostnames Django will accept requests for."
read -p "Allowed hosts [$DEFAULT_HOSTS]: " ALLOWED_HOSTS
ALLOWED_HOSTS="${ALLOWED_HOSTS:-$DEFAULT_HOSTS}"

echo ""
echo "CSRF_TRUSTED_ORIGINS is needed if you access the Pi via a URL with a port."
DEFAULT_ORIGINS="http://127.0.0.1:8000"
[ -n "$LOCAL_IP" ] && DEFAULT_ORIGINS="$DEFAULT_ORIGINS,http://$LOCAL_IP:8000"
[ -n "$TAILSCALE_IP" ] && DEFAULT_ORIGINS="$DEFAULT_ORIGINS,http://$TAILSCALE_IP:8000"
read -p "CSRF trusted origins [$DEFAULT_ORIGINS]: " CSRF_ORIGINS
CSRF_ORIGINS="${CSRF_ORIGINS:-$DEFAULT_ORIGINS}"

echo ""
echo "STREAM_HOST is the hostname the browser uses to reach the video stream (port 8765)."
echo "Usually the same IP you use to reach the Pi."
read -p "Stream host [${LOCAL_IP:-127.0.0.1}]: " STREAM_HOST
STREAM_HOST="${STREAM_HOST:-${LOCAL_IP:-127.0.0.1}}"

cat > "$ENV_FILE" <<EOF
DJANGO_SECRET_KEY=$SECRET_KEY
DJANGO_ALLOWED_HOSTS=$ALLOWED_HOSTS
CSRF_TRUSTED_ORIGINS=$CSRF_ORIGINS
STREAM_HOST=$STREAM_HOST
STREAM_PORT=8765
EOF

echo ""
echo ".env written to $ENV_FILE"

# --- Step 4: Quick check ---
echo ""
echo "Running Django system check..."
cd "$REPO_DIR/remote_control"
export $(cat "$ENV_FILE" | xargs)
"$VENV_DIR/bin/python3" manage.py check 2>&1 || true

echo ""
echo "=== Setup complete ==="
echo ""
echo "To run:"
echo "  cd $REPO_DIR/remote_control"
echo "  source $VENV_DIR/bin/activate"
echo "  export \$(cat $ENV_FILE | xargs)"
echo "  python3 manage.py runserver 0.0.0.0:8000"
