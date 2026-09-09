import datetime

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class BlogSchema(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    slug: str = Field(min_length=1, max_length=255)
    description: str
    body_content: str

    status: str = "draft"

    meta_title: Optional[str] = Field(
        default=None,
        max_length=255
    )

    meta_description: Optional[str] = None


class BlogResponseSchema(BaseModel):
    id: int

    title: str
    slug: str
    description: str
    body_content: str

    status: str

    published_at: Optional[datetime.datetime] = None

    meta_title: Optional[str] = None
    meta_description: Optional[str] = None

    created_at: datetime.datetime
    updated_at: datetime.datetime



class BlogUpdateSchema(BaseModel):
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    slug: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    description: Optional[str] = None
    body_content: Optional[str] = None

    status: Optional[str] = None

    published_at: Optional[datetime.datetime] = None

    meta_title: Optional[str] = Field(
        default=None,
        max_length=255
    )

