from pydantic import BaseModel


class AuthData(BaseModel):
    email: str
    password: str
