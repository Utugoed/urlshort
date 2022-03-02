from pydantic import AnyHttpUrl, BaseModel, EmailStr, Field
from typing import Optional


class LinkCreateModel(BaseModel):
    url: AnyHttpUrl = Field(
        ..., title="URL", description="The URL to which the user will be redirected."
    )


class LinkModel(LinkCreateModel):
    id: str = Field(None, title="ID", description="Saved link ID.")
    link: str = Field(
        None, title="Link", description="A short link to use in the final address."
    )
    owner: str = Field(
        None, title="Owner", description="The ID of the user who created the link. "
    )
