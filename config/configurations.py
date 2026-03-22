from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    HOST = os.getenv('DB_HOST')
    USER = os.getenv('DB_USER')
    PORT = os.getenv('DB_PORT')
    PASS = os.getenv('DB_PASS')
    NAME = os.getenv('DB_NAME')

    @property
    def sync_db_url(self):
        return f'postgresql+psycopg://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}'

    @property
    def async_db_url(self):
        return f'postgresql+asyncpg://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}'


settings = Settings()
