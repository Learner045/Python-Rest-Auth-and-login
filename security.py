
from Authentication.user import User
from werkzeug.security import safe_str_cmp

users=[
   User('bob','asdf',1)
]

username_mapping={
   u.username : u for u in users  #list comprehension for mapping username with user obj
}

userid_mapping={
    u.id:u for u in users
}

def authenticate(username,password):
    user = username_mapping.get(username,None) #get user object
    if user and safe_str_cmp(user.password,password): #user obj has passowrd field as mentioned in User class
        return user

def identity(payload): #func is unique to flask JWT
    user_id=payload['identity'] #payload contains identity info about user
    return userid_mapping.get(user_id,None)