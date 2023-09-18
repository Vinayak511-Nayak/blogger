from blogproject import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(45),unique=True,index=True)
    username= db.Column(db.String(45),unique=True,index=True)
    password_hash=db.Column(db.String(100))
    profile_pics = db.Column(db.String(),default='default.jpg')
    blogpost= db.relationship('BlogPost', backref='author',lazy=True)

    def __init__(self,email,username,password):
        self.email=email
        self.username=username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"email:{self.username}"

class BlogPost(db.Model,UserMixin):
    users = db.relationship(User)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    blog = db.Column(db.String)
    current_time = db.Column(db.Integer)
    current_date= db.Column(db.Integer)
    user_id= db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    def  __init__(self,title,blog,current_date,current_time,user_id):
        self.title= title
        self.blog = blog
        self.current_date= current_date
        self.current_time = current_time
        self.user_id=user_id
        
    def __repr__(self):
        return f"{self.title}---{self.blog}"
