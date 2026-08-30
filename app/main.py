#DAY 1... 




from fastapi import FastAPI , Response ,status, HTTPException , Depends
from fastapi.params import Body # Import Body so FastAPI knows to read data from the request body.
# It converts the incoming JSON into a Python dictionary (or a Pydantic model later).
from pydantic import BaseModel
from typing import Optional , List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from .router import post, user , auth , vote
from .config import settings 


import time
from sqlalchemy.orm import Session 
from . import models , utils , oauth2
from .database import engine , Base , sessionlocal 
from .database import get_db 
from .import schemas


from fastapi.middleware.cors import CORSMiddleware

#models.Base.metadata.create_all(bind = engine) #creates a table if already not existent .. 

#we actually dont need the above statement any more since we have already put alembic in rn .. but its okay to leave it since it just creates our tables first and alembic is used only to update the tables / create new ones later on .. 
#this is was used when we only had sqlALcemhy we will prefer nto to use this anymore..  since we have alembic..al



#creating a instance of fastapi
# do uvicorn main(file nanme) : app (instance name) .. to create aweb server where this runs 
app = FastAPI()
origins = ["https://www.google.com" , "https://www.youtube.com"]  #if we want public api that everyone can access then do ["*"];
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





# not using this any longer since have started using sql alchemy the below part.. 

# while True:
# #now again better to put whole try and excpet block in a while loop cause if we dont it just shows error and continues with fast api methods which makes no sense 
# #connect to a existing data base using adaptor 
#     try:

#         conn = psycopg2.connect(host = "localhost" , database = 'fastapiproj' , user = 'postgres' , password= 'root1234' )  #host = ' # host -> Address of the PostgreSQL server.
# # "localhost" means the database is running on this computer. ' databse = name of database username is default one and pasword is my postgress admin password


# #also the problem of this library is we cant see columns name with can just retreive data so to avoid that we import RealDictCursor .. and in my connection do cursor_factory = RealDictCursor 
# #Open a cursor to perform database operations and put that thing to get colums in it its considered a better practice than putting it in my connecition cmd itseld
#         cur = conn.cursor(cursor_factory= RealDictCursor)
#         print('databse connection was succesful')
#         break
#     except Exception as error:
#         print('connection databse failesd')
#         print('error')
#         time.sleep(2) # so it will retry every 2s if it fails so basically supose my net is fucked then it will try again and again ... but if password is wrong it wil fail everytime ...




#now after doing all the below function until get posts... irl we have to save our posts so we can retreive them irl we use databses but we havent learnt it for now so we sotr ehtem in a array 
#not using my_posts anymroe since we created our data base.. 
#my_posts = [{"title" : "title of post 1 " , "content " : "content of post 1 " , "id" : 3} , { "title2" : "fav food" , "content " : " i love pizzas" , "id" : 2}] #for nwo we have hardocded 

#the code below is called as a path operation or route.. consists of two major things a function and decorator'@'
@app.get("/")  #get is the http method ... and("/") is the root path basically path after domain name of api... 
async def root():  
    return {"message": "Welcome to my APi !! "} #data sent back to the user which fast api convert it into json and shows it 
# decorater is used to make the function act like api...

#every time we make a change restart your serverby ctrl+c and  running uvicorn main:app in terminal to reflect changes in our web page.. 
#or do uvicorn main:App --reload.. this will auto reload after every save 


#test to see if depndencies workds.. 
@app.get("/sqlalchemy") # "/sqlalchemy cause its our endpoint /databsse.. "
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return  posts  
   




#since we have moved all our functions into router directory ... we need to acess their operations in our main.py file for that .. we did all this because to keep our main.py file clean and all the above code with operations are just tests and hold no meaning 
#app is our fastapi object we difined .. 

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


