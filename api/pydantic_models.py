from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class ModelName(str, Enum):
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"

class QueryInput(BaseModel):
    question: str
    session_id: str = Field(default=None)
    model: ModelName = Field(default=ModelName.GPT_4O_MINI)

class QueryResponse(BaseModel):
    answer: str
    session_id: str
    model: ModelName

class DocumentInfo(BaseModel):
    id: str
    filename: str
    upload_timestamp: datetime

class DeleteFileRquest(BaseModel):
    file_id: int 