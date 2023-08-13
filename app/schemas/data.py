from pydantic import BaseModel


class MessageStatus(BaseModel):
    status: str
    message: str
