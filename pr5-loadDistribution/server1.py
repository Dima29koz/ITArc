from server.app import create_app
from server.config import BaseConfig


if __name__ == '__main__':
    app = create_app(BaseConfig, '1')
    app.run(port=5001)
