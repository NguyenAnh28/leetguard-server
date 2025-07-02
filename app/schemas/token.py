from pydantic import BaseModel

# Schema for authentication tokens. Used to return access and refresh tokens after login or refresh.
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str