from typing import Optional, Dict
from pydantic import BaseModel
from models.status import Status


class Submission(BaseModel):
    id: int
    language: str
    code: str
    stdin: Optional[str] = None
    output: Optional[Dict] = None
