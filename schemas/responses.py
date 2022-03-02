from pydantic import BaseModel, Field
from typing import Optional


class ResponseModel(BaseModel):
    status: str = Field(default="OK", title="Status", description="Operation status.")
    id: Optional[str] = Field(
        None,
        title="ID",
        description="The ID of the object with which the interaction was performed.",
    )
    detail: Optional[str] = Field(
        default="No detail",
        title="Detail",
        description="Learn more about the reasons for the failure of the operation.",
    )
