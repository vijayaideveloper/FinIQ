from pydantic import BaseModel,EmailStr



class SignUp(BaseModel):
    name : str
    age : int
    city : str
    email : EmailStr
    password : str 

