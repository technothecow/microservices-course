from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, datetime
from uuid import UUID

class UserRegistration(BaseModel):
    login: str
    password: str
    email: EmailStr


class Authentication(BaseModel):
    login: str
    password: str


class UserProfile(BaseModel):
    id: UUID
    login: str
    email: EmailStr
    name: Optional[str] = None
    surname: Optional[str] = None
    date_of_birth: Optional[date] = Field(None, alias="dateOfBirth")
    phone_number: Optional[str] = Field(None, alias="phoneNumber")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    class Config:
        populate_by_name = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    date_of_birth: Optional[date] = Field(None, alias="dateOfBirth")
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(None, alias="phoneNumber")

    class Config:
        populate_by_name = True


class Error(BaseModel):
    code: int
    message: str