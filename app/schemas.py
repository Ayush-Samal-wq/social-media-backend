from pydantic import BaseModel , EmailStr , Field , ConfigDict
from datetime import datetime
from typing import Optional
from pydantic import conint


#pydantic schema model / basemodel on how our post should llok like  # its gonna valiudate if the input by user is in right format .. 
class PostBase(BaseModel):
    title: str
    Content: str # data type of the contnet .. /fieldtype..
    published : bool = True #what we did here was we created a published req where if user dosent mention published then its default is true if he sets as false then itsnt gonna get published...
    # rating : Optional[int] = None # this is optional function from typing library ie if ratings is mentioned and is a int then it will show else it just defaults to none it not a compulsory field ..  removing it when we go into data base section since we dint need it in our database..

class CreatePost(PostBase):  #basically using inheritance concept.. 
    pass

# we can create such classes and supose i want to do a update post but only thing allowed to updates is published i could inherit all the stuff from postBase and only keep update field in my unction like 
#class UpdatePost(postbase):
#published : bool   #for now we are usign creatpost for both update and create since its the same format used.. 

#response model for userCreate.. 
class UserCreateresp(BaseModel):
    id : int
    email: EmailStr
    created_at : datetime
    model_config = ConfigDict(from_attributes=True)
    
#to create a repsonse modell .. 
#here we could have named post as responsepost or anything but since we are returning post everywhere it makes sense to name it as such if or else i have to go and change everywhere return post to return response post 
class post(PostBase): # to acess our repsonse model besides our path operationg of any fucntion mention response_mode = schemas.post...
    id : int
    #title : str # id ot need to mention title contetn adn published since it extends / inherits from postbase class nayway just for my readability //
    #Content : str
    #published : bool
    Created_at : datetime
    owner_id : int

    owner : UserCreateresp
    # Return the related User object in the format of UserCreateresp.
    # FastAPI gets it from post.owner (created by relationship()). 
    model_config = ConfigDict(from_attributes=True) #instead of orm mode use this in new pydantic version 

#before this in response we used to get id and all that now we dont .. and only get titile contetn and publiushed values .. if we want ids and all we can specify like above 
#now we know that in general pydatic always excpects dict return values so it will trhow error when we try to return this so for this we need to turn on ***ORM MODE***
#so we use class config orm mode = true thing .. 
#so orm_mode of pydantic will tell it to read data even if its not a dictionary 



class Usercreate(BaseModel): # this is how the input of the user should be
    email : EmailStr # validates if its a email or no . 
    password : str



class postoutwithvotes(BaseModel):
    post : post
    total_votes : int

    model_config = ConfigDict(from_attributes=True)


#creating a schema for how our user will input login creds.. 
class UserLogin(BaseModel):
    email : EmailStr
    password : str

#response model for token send back .. 
class TokenResp(BaseModel):
    access_token:str
    token_type : str

class TokenData(BaseModel):
    id : Optional[str] = None



#schema for how our body will be when we send in a vot .. 
class Vote(BaseModel):
    post_id : int
    dir: conint(ge=0, le=1) # to ensure that votes dir is only 1 or 0 .. 