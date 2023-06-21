from dataclasses import dataclass
from typing import Optional

from backend.web.config.AuthorizationConfig import AuthorizationConfig
from backend.web.config.SessionConfig import SessionConfig


@dataclass
class Config:
    authorization: AuthorizationConfig
    session: Optional[SessionConfig] = None
