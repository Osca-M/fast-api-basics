import uuid
from typing import Optional

from pydantic import BaseModel


class Blog(BaseModel):
    id: Optional[uuid.UUID]
    title: str
    body: str
    published: bool
