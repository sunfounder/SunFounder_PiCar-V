from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    auth_password: str = "picar"
    jwt_secret: str = "change-me-in-production"
    jwt_expiry_hours: int = 24

    picar_host: str = "localhost"
    picar_port: int = 8000
    picar_stream_port: int = 8765

    # Set to a socks5 URL if Tailscale userspace networking is in use
    # e.g. "socks5://127.0.0.1:1055"
    proxy_url: str = ""

    # Mock mode — when True, return fake data instead of proxying to the Pi.
    # Useful for local frontend development.
    mock_mode: bool = False

    model_config = {"env_prefix": "RELAY_"}


settings = Settings()
