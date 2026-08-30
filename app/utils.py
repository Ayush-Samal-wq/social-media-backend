from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"] , deprecated = "auto")

def hashpwd(password : str):
    return pwd_context.hash(password)

def verify(plain_password , hashed_password):
    return pwd_context.verify(plain_password , hashed_password) # user enters a password in login portal we hash it and then we compare it with the hashed form password of the user stored in the data base using verify()
