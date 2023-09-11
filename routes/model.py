from pydantic import BaseModel, Field


class ProfileRequest(BaseModel):
    email: str = Field(min_length=3, max_length=50, pattern=r'^[\w._-]*@[\w]*.[a-zA-Z]{2,4}$')
    password: str = Field(min_length=3, max_length=50)


class StatusResponse(BaseModel):
    success: bool
    message: str
