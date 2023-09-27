from dataclasses import dataclass


@dataclass
class Config:
    host: str = "127.0.0.1"
    port: int = 8000
