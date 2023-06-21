import os

from backend.web.Application import Application
import backend.web as web


if __name__ == "__main__":
    app = Application()
    web.run_app(app, config_path=os.path.join(os.path.dirname(__file__), 'config.yml'))
