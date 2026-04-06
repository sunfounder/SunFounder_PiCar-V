FROM python:3.12-slim

# Install Tailscale
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    curl -fsSL https://tailscale.com/install.sh | sh && \
    apt-get remove -y curl && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml .
COPY relay/ relay/
COPY static/ static/
RUN pip install --no-cache-dir .

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
