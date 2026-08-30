from fastapi import APIRouter , Depends , status , HTTPException , Response
from ..database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 
from .. import schemas , models , utils , oauth2

router = APIRouter(
    tags=['AUTHENTICATION']
)

@router.post("/login"  , response_model= schemas.TokenResp)
#def login(user_cred : schemas.UserLogin ,  db: Session = Depends(get_db)) this insteadof using a schema we will now use oAuthPasswordRequestForm which will ask for a username and password so we need ot compare our email to the username ..
def login(user_cred : OAuth2PasswordRequestForm = Depends() ,  db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_cred.username).first()
    
    if not user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN , detail= f"Invalid cred")
    
    if not utils.verify(user_cred.password , user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN ,  detail  = f"Invalid cred")
    
    access_token = oauth2.create_access_token(data = {"user_id" : user.id} )
    return {"access_token" : access_token , "token_type" : "bearer"}
        



