from .database import Base
from sqlalchemy import Column , Integer , VARCHAR ,String , Boolean , TIMESTAMP , ForeignKey## need to import all datatypes req.. 
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
 
class Post(Base): # this is my pythoni class based of of Base.. 
    #bvelow we create our table using sqlalcemy 
    __tablename__ = 'posts'
    id = Column(Integer , primary_key= True , nullable= False )
    title = Column(VARCHAR(100) , nullable= False)
    content = Column(String , nullable = False)
    published = Column(Boolean ,  server_default =  'True' , nullable = False)
    created_at = Column(TIMESTAMP(timezone=True) , nullable = False , server_default= text('now()'))  #no commas at end to seperate each col since it acts a tuple f we do it 
    owner_id = Column(Integer , ForeignKey("users.id" , ondelete="CASCADE") , nullable= False) #wont updaate since sqlalchemy not meant for this 
    # ^^Stores the ID of the user who owns this post.
    owner = relationship("Users") 
    # SQLAlchemy relationship -> lets us access the User object from a Post (post.owner)
    # It uses owner_id (ForeignKey) behind the scenes to fetch the matching user.
# to use this above table  in mains.py we write models.metadata.create_all(bind = engine)
# create_all() reads our models and creates tables that DON'T already exist.
# It does NOT update an existing table when we later change its model.
#To update we have to use alembic a Databse Migration tool .. 
 
#so for now we are just deleting the whole post tabel and re running this code to get the table. // with owner id later will use alembic we could do this from pg admin as well . 




#now we are going to create a orm model for registering users so step 1 is creatign atbale.. 
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer , primary_key= True , nullable= False )
    email = Column(String , nullable = False , unique = True)
    password = Column(String , nullable = False)
    created_at = Column(TIMESTAMP(timezone = True) , nullable = False ,server_default=text('now()'))

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete= "CASCADE"), primary_key=True)
    post_id = Column(Integer , ForeignKey("posts.id" , ondelete="CASCADE") , primary_key= True)