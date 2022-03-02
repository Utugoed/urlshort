from pydantic import BaseModel, Field


class UserAuthModel(BaseModel):
    access_token: str = Field(None, title="Token", description="Access token.")
    token_type: str = Field(None, title="Token type", description="Token type.")
