from pydantic import BaseSettings


class Settings(BaseSettings):
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    DOMAIN: str = "urlshort.appvelox.ru"
    MONGO_DB: str = "FAPITraining"
    SECRET_KEY: str = "oS0nLHkXeA72lwDOmzmhqcg8yngjvU3a0VtMDlGqCdpDexmx"
    MONGODB_CONNECTION_URL: str
    LINK_LENGTH = 6

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
