from dataclasses import dataclass


@dataclass
class SessionConfig:
    key: str
    launcher_token: str
