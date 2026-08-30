from fastapi import FastAPI , Response, status , HTTPException , Depends  ,APIRouter
from sqlalchemy.orm import Session
from ..import models,  schemas , utils
from ..database import get_db

#now we use routers instead of app in this file because we want to set a router for each file from where we can acess these functions and path operation in our main file ihtout cluttering it 
router = APIRouter(
    prefix= "/users",
    tags= ['USERS']
) 
# and now replace @app with router 

@router.post("/" , status_code = status.HTTP_201_CREATED , response_model= schemas.UserCreateresp) 
def create_user(user : schemas.Usercreate , db :Session = Depends(get_db)):

    hashed_password  = utils.hashpwd(user.password)
    user.password = hashed_password

    new_user = models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}" , response_model= schemas.UserCreateresp)
def get_user(id : int, db :Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"User with id {id} does not exist ")
    
    return user
