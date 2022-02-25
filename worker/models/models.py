from typing import Optional
from pydantic import BaseModel


class Submission(BaseModel):
    id: int
    language: str
    code: str
    stdin: Optional[str] = None
