from pydantic import BaseModel,EmailStr


class CreateIncome(BaseModel):
    email : EmailStr
    title : str
    amount : float

class ReadIncome(BaseModel):
    email : EmailStr

class UpdateIncome(BaseModel):
    id : int
    email : EmailStr
    title : str
    amount : float


class DeleteIncome(BaseModel):
    id : int
    email : EmailStr