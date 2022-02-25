from typing import Optional, Dict
from pydantic import BaseModel


class Submission(BaseModel):
    id: int
    language: str
    code: str
    stdin: Optional[str] = None
    output: Optional[Dict] = None
