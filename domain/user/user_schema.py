from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo

class UserCreateSchema(BaseModel):
    username: str
    password: str
    confirm_password: str
    email: EmailStr

    @field_validator("username", "password", "confirm_password", "email")
    @classmethod
    def not_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Username cannot be empty.")
        return value

    @field_validator("confirm_password")
    @classmethod
    def validate_password(cls, value: str, info: FieldValidationInfo) -> str:
        if 'password' in info.data and info.data['password'] != value:
            raise ValueError("Password and confirm password do not match.")

        return value
