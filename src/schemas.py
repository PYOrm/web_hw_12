from pydantic import BaseModel, Field, EmailStr, PastDate


class ContactModel(BaseModel):
    name: str = Field(max_length=50)
    soname: str = Field(max_length=50)
    email: EmailStr = Field(max_length=100)
    phone: str
    birthday: PastDate
    info: str = Field(max_length=255)


class ContactResponse(ContactModel):
    id: int

    class Config:
        from_attributes = True


class UserModel(BaseModel):
    name: str = Field(max_length=50)
    email: str = Field(EmailStr)
    password: str


class UserDb(UserModel):
    id: int
    update_token: str | None

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
