from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    HOST = os.getenv('DB_HOST')
    USER = os.getenv('DB_USER')
    PORT = os.getenv('DB_PORT')
    PASS = os.getenv('DB_PASS')
    NAME = os.getenv('DB_NAME')
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    APP_URL = os.getenv('APP_URL')
    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = os.getenv('REDIS_PORT')
    REDIS_DB = os.getenv('REDIS_DB')

    @property
    def sync_db_url(self):
        return f'postgresql+psycopg://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}'

    @property
    def async_db_url(self):
        return f'postgresql+asyncpg://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}'


settings = Settings()
