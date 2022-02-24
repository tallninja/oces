from typing import Optional
from pydantic import BaseModel


class Submission(BaseModel):
    language: str
    code: str
    stdin: Optional[str] = None
