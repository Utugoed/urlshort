from pydantic import BaseModel, Field


class RedirectModel(BaseModel):
    link: str = Field(
        None,
        title="Link",
        description="ID of the short link that will be used in the final address.",
    )
    ip: str = Field(
        None, title="IP", description="IP of the user who used the short link"
    )
