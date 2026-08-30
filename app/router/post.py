from fastapi import FastAPI , Response, status , HTTPException , Depends  ,APIRouter
from sqlalchemy.orm import Session 
from typing import List , Optional
from ..import models,  schemas , utils , oauth2
from ..database import get_db
from sqlalchemy import func

#now we use routers instead of app in this file because we want to set a router for each file from where we can acess these functions and path operation in our main file ihtout cluttering it 
router = APIRouter(
    prefix= "/posts",#by doing this in our path route we dont need to metnion /posts everytime .. and just mention the things after it  "/post" will be doneted by "/"
     tags=['POSTS'] 
    
) # and now replace @app woth router 


#lets create a new path oper... to get the posts made by a user
@router.get("/" ) 
def get_posts(db : Session = Depends(get_db) , current_user : int = Depends(oauth2.get_current_user) , limit : int = 10,skip : int = 0 , search : Optional[str] = ""):
    #cur.execute("""SELECT * FROM posts""") #now that we have a adaptor we can start doing sql queseies through cur.. 
    #posts = cur.fetchall() # once we execute we need to fetch since we want all posts we use fetchall  
    print(current_user.email)
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all();  we will use the same thing but include joins as well below since we want to count no of votes as well . 
    results = db.query(models.Post,  func.count(models.Vote.post_id).label("total_votes")).join(models.Vote , models.Vote.post_id == models.Post.id , isouter= True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(results)  
    # Why we are returing like this -> Convert each SQLAlchemy query result (Row) into our Pydantic response schema so the returned data matches the expected API response format.
    return[
        schemas.postoutwithvotes(
            post=schemas.post.model_validate(row.Post),
            total_votes= row.total_votes

        )
        for row in results
    ]
# fast api always runs the first match so if we have same path for two diff fucntions then the first match runs .. 


#using POST https method to create posts.. 
'''###@app.post("/createposts")   
def create_posts(content: dict = Body(...)): # Body(...) tells FastAPI to expect JSON data which gets converted in a python dictonary and storedi in variable ocntent 
   # return content
    return{"newpost":f" title{content['title']} content{content['info']}"}'''


#so instead of doing the above creaTE POST MTHOD WHAT WE CAN DO IS USE OUR PYDANTIC BASE MODEL... 

@router.post('/' , status_code = status.HTTP_201_CREATED , response_model= schemas.post ) # '/createposts path name is not good naming convention since we are just posing so we change our path to posts... 
async def create_posts(new_post : schemas.CreatePost , db : Session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user)  ): # here Post on the right is my pydantic model class ... so i am referencing it and saving it .. as new_post (which is the actual object FastAPI creates from the incoming JSON... )
    #print(new_post.published) # this were we are prinnting in our terminal to verify if its working 
    #print(new_post.model_dump()) # this is used to just ocnvert everythign in new_post into a dictonary if we ever need and w ecan return it as below so that dict is shwon on fron edn as well .. 
    #new_post_dict = new_post.model_dump() 
    #new_post_dict['id'] = randrange(0, 100000) # setting id 
   #my_posts.append(new_post_dict) #adding  to myposts..  COMMENTED IT ALL CAUSE NO USE OF THIS NOW THAT WE ARE DIRECTLY OCNNECTING WITH DATABASE.. 

    #cur.execute("""INSERT INTO posts (title , content , published ) VALUES(%s , %s , %s) RETURNING *  """, (new_post.title , new_post.content , new_post.published))
    #new_post = cur.fetchone() #ALSO AFTER ALL THIS IT STILL WONT GET UPDATED IN DATABSE WE NEED TO COMMIT THE CHANGES   #THE %S ABOVE ACT AS PLACEHOLDERS TO AVOID SQL INJECTION WHERE USER MIGHT GIVE A SQL QUERY AS A INPUT AND IT MIGHT MANIPULATE OUR DATABASE
    #conn.commit()    # need to commit it so that changes reflect in data base.. 
    
    #post_made_by_sqlal =  models.Post(title = new_post.title, Content = new_post.ontent , published = new_post.published ) # but we cant type the whole thing suppose we had 50 fields so better is to unpack the post.. 
    print(current_user.email)
    post_made_by_sqlal = models.Post( owner_id = current_user.id ,  ** new_post.model_dump()) #lot cleaner and if we add fields in models table then it will auto update here .. 
    db.add(post_made_by_sqlal)
    db.commit()
    db.refresh(post_made_by_sqlal )


    return post_made_by_sqlal  #check iska output on postman ..  #this is what is seen on postman / frontend  # we are returning the post we just made 
#we can also seeuppose s in postman body we remove the content part then we can see a error comming notifying us abouut the missing content and shows a 422 error here in our terminal signifying unprocessable content
    #so we can see its validation process..



#DAY 2....... 
#def find_post(id):
    #for post in my_posts:
        #if post['id'] == id:
            #return post

# now we continue with our crud application we create a operation to rerieve one individual post.. 
@router.get("/{id}" , response_model= schemas.postoutwithvotes) #{id} cause we are getting a specific post based on the posts id provided by user.. [CALLES A PATH PARAMETER]
async def get_post(id : int , db :Session = Depends(get_db) ,current_user : int = Depends(oauth2.get_current_user)): # as you can see by naming conv its singluar not get posts as the one above.. since we are gettgina  singular post 

    #cur.execute(""" SELECT * FROM posts WHERE id = %s """ , (str(id), ))  # we convert id into str after taking as integer so that we can validate that user has put a id only as a integer and not any string once that is odne our systme converts it inot a string.. 
    ##post = cur.fetchone() 
    #print(post)
    #post = find_post(id) # instead of doing int(id) where we are converting number since we had defeined id as a str into integers we can do validation in the above line by just typing id : int which automatically checks wether somehting can be converted into a int or no 
    
    #USING SQL ALCMEHY .. TO QUERY .. 
    post = db.query(models.Post , func.count(models.Vote.post_id).label("total_votes")).join(models.Vote , models.Vote.post_id == models.Post.id , isouter= True).group_by(models.Post.id).filter(models.Post.id == id).first()
    print(post)
    if not post:
        #Response.status_code = status.HTTP_404_NOT_FOUND;  # we can always manually set up a error but not advised its always advised to raise a http exception....  #here you need to pass response in function and import Response and status from Fastapi.. 
        #return {'message' :f"post with id {id} was not found..."}; 

        #always prefer settign up a exception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail= f"post with id {id} not found.. try searching with a valid id.. ") 
        
    return  schemas.postoutwithvotes(
                post = schemas.post.model_validate(post.Post),
                total_votes =  post.total_votes  
        )
        #also no squre brackets since we arent returning a list of posts here compare with the pprev response model of get all posts.. 
        #for row in post #we did this in get all posts because query returns multiple rows.. but here for one id .. there will be only one post.. right so nothign to loops over 
     #if id was entered as a random wjdufjsfh then it will just show the error similar to a schema validation  error .. 



#WE ARE NOW CREATING SOMETHING TO DELETE A POST .. 

#def find_post_index(id):
    #for i ,  p in enumerate(my_posts): # enumerate gives indexes to the posts in my_post when looping through since we delete it based of the indx in the my_posts but no need of all these just use sql .. 
        #if p['id'] == id :
         #   return i


@router.delete("/{id}" , status_code= status.HTTP_204_NO_CONTENT)
async def delete_post(id :int , db :Session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user)):
    #deleting ... 
    #first find the index in the array that has req id and then my_post.pop()
    #index = find_post_index(id)
    #cur.execute(""" DELETE FROM posts WHERE id = %s RETURNING *   """ , (str(id), )) # returning * gives us the what was the post before it was deleted ..
    #deletedpost = cur.fetchone() #since we are tyring to fetch the one deleted post ..     
    #conn.commit() # so that the change of post is registered in databse.. 
    deletedpost = db.query(models.Post).filter(models.Post.id == id)
    post = deletedpost.first()
    if(deletedpost == None):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail = f"post with id no - {id} not found pls give a valid id .. ")
    #my_posts.pop(index) this was all when when we didnt have a databse so .. no need of these stuff rn.. 
    deletedpost.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)  #{'message' : 'successfully deleted the post...'}  since we dont return any text / content when we are using a 204 error ... so just return the status code that is no contetn here 

    

#FINAL CRUD OPERATIONS IS UPDATE POSTS... 
@router.put("/{id}" , response_model= schemas.post)
async def update_posts(id :int , updated_post : schemas.CreatePost , db : Session = Depends(get_db) , current_user : int = Depends(oauth2.get_current_user)):
    #using our schema to make sure proper updates occur.. 
    #index = find_post_index(id)
    #cur.execute(""" UPDATE posts  SET title = %s , content  = %s , published = %s WHERE id = %s RETURNING * """ , (  post.title , post.content , post.published , id ))  #doing post. cause we are using Post schema which has been set to post
    #updated_post = cur.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post  = post_query.first() #grabbing origninal post 
    if(post == None): #if it dosent exits.. 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail = f"post with id no - {id} not found pls give a valid id .. ")
    #so if post exits we update it .. 
    post_query.update(updated_post.model_dump() ) # not using **updated_post.modeldump() because update() expects a mapping (dictionary), whereas ** unpacks the dictionary into separate keyword arguments.
    db.commit()

    #if it exists .. 
    
 #  post_dict = post.model_dump()      # Convert the Pydantic Post object into a normal Python dictionary.
 #  post_dict["id"] = id               # Add the id from the URL since the request body doesn't contain an id. 
  # my_posts[index] = post_dict        # Replace the old post at this index with the updated dictionary.
   
    return  post_query.first()