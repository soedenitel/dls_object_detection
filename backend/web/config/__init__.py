import random
from hashlib import sha256

import yaml
import typing

from backend.web.config.AuthorizationConfig import AuthorizationConfig
from backend.web.config.Config import Config
from backend.web.config.SessionConfig import SessionConfig

if typing.TYPE_CHECKING:
    from backend.web import Application


def setup_config(app: "Application", config_path: str):
    with open(config_path, "r") as f:
        yaml_config = yaml.safe_load(f)

    app.config = Config(
        authorization=AuthorizationConfig(
            login=yaml_config["authorization"]["login"],
            password=sha256(yaml_config["authorization"]["password"].encode()).hexdigest(),
        ),
        session=SessionConfig(
            key=yaml_config["session"]["key"],
            launcher_token=str(random.randint(0, 65535))
        )
    )
    del yaml_config
