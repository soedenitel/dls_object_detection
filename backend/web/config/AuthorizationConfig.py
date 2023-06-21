from dataclasses import dataclass


@dataclass
class AuthorizationConfig:
    login: str
    password: str
