from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_code = db.Column(db.String(255))
    posts = db.relationship('Post',backref = 'user', lazy = 'dynamic')
    comments = db.relationship('Comment',backref = 'user',lazy = "dynamic")
   
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_code = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_code,password)    

    def __repr__(self):
        return f'User {self.username}'

class Post(db.Model):
    __tablename__='posts'

    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String)
    post = db.Column(db.String)
    time = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    post_comments = db.relationship('Comment',backref = 'post',lazy = "dynamic") 

    def save_post(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_post(cls,id):
        
        post = Post.query.filter_by(id=id).first()
        
        return post     

    def __repr__(self):
        return f'User {self.title}'

class Comment(db.Model):
    __tablename__='comments'

    id = db.Column(db.Integer,primary_key = True)
    post_comment = db.Column(db.String)
    post_id = db.Column(db.Integer,db.ForeignKey("posts.id")) 
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))        

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(pitch_id=id).all()
        return comments        
