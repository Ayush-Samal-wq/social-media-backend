from jose import JWTError , jwt 
from datetime  import datetime , timedelta
from . import schemas , models , utils , database
from fastapi import Depends , HTTPException , status
from fastapi.security import OAuth2PasswordBearer 
from sqlalchemy.orm import Session
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") #basicall y token url is our end point so we want our end point to always be login /login remove the slash 


#3 impo things to be provided..
#SECRET KEY IS NEED # this exists on the api and only known in the api used to form test sginature and compare bascialyl the behind the scene mai use hot ahai ye of.verify() in auth file / util file .. 
#algorithm to be used   
#expiration time 

SECRET_KEY = settings.secret_key #randome .. 
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy() # sicne we dont wanna accidentally modify orgininal data.. 
    expire = datetime.now()  + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY , algorithm= ALGORITHM)

    return encoded_jwt


#once the access_token has been created we need to verify it .. 
def verify_access_token(token : str , credentials_exception):
    try:
        payload = jwt.decode(token , SECRET_KEY , algorithms= [ALGORITHM]) # so one its decoded it just becomes a dictionary with payload object so now we identify which user it belongs by gettgin id 
        id :str = str(payload.get("user_id"))

        if id is None:
            raise credentials_exception
        token_data  = schemas.TokenData(id = id)
    except JWTError:
        raise credentials_exception
    return token_data
    
#the obv function is to verify but we need to call it using get_current_user() what this fucntion does is before we do anything we always need to be authorized to do so so f we want to protect osmethign we always verify the user first and to do so we call this 
def get_current_user(token :str = Depends(oauth2_scheme) , db:Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED , detail= f"could not validate user " , headers={"WWW-authenticate" : "Bearer"})

    token = verify_access_token(token , credentials_exception) #since we return token data that only consists id we get token = id .. 
    user = db.query(models.Users).filter(models.Users.id == token.id).first()

    return user
 
#How we use this ... suppose we want to make sure tha t aperson logs in before creating a post 
#async def create_posts(new_post : schemas.CreatePost , db : Session = Depends(get_db) , user_id: int = Depends(oauth2.get_current_user)): we just add get curret user as a dependencies 




# JWT AUTH FLOW:
# LOGIN -> verify email/password -> put user_id in JWT -> send token to user.
# PROTECTED ROUTE -> oauth2_scheme gets token -> get_current_user() calls verify_access_token()
# -> decode JWT -> extract user_id -> TokenData(id) -> authenticated user identified.