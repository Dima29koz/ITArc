from app import create_app
from config import BaseConfig

app = create_app(BaseConfig, '0')

if __name__ == '__main__':
    app.run()
