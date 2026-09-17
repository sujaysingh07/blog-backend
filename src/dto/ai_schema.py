
from pydantic import BaseModel

class BlogRequest(BaseModel):
    topic: str


class BlogGeneratedResponse(BaseModel):
    title: str
    slug: str
    short_description: str
    content: str
    status: str
    meta_title: str
    meta_description: str