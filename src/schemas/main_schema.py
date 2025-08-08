from pydantic import BaseModel, HttpUrl
from typing import List

class HackRXRequest(BaseModel):
    documents: HttpUrl
    questions: List[str]
