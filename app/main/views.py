from flask import render_template, request,redirect,url_for,abort,flash
from . import main
from ..models import User,Post,Comment
from .forms import UpdateProfile,PostForm,CommentForm
from .. import db
from flask_login import login_required,current_user
from datetime import datetime
from ..request import get_random_quote

@main.route('/')
def index():
    posts = Post.query.order_by(Post.time.desc()).all()
    quote = get_random_quote()

    return render_template('index.html', posts = posts,quote=quote)
    
@main.route('/add',methods = ['GET','POST'])
@login_required
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(title = form.title.data, post = form.post.data,user=current_user)
        
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('main.index'))
         
    return render_template('add.html',post_form=form)

@main.route('/post/<int:id>')
def post(id):

    post = Post.query.filter_by(id=id).first()
    comments = Comment.get_comments(post.id)

    return render_template('post.html',comments = comments, post = post)

@main.route('/post/<int:id>/update',methods = ['GET','POST'])
@login_required
def update(id):
    post = Post.query.filter_by(id=id).first()
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.post = form.post.data
        db.session.commit()
        return redirect(url_for('main.post',id=post.id))
    elif request.method == 'GET':    
        form.title.data = post.title
        form.post.data = post.post  
    return render_template('add.html',post_form=form)

@main.route('/post/<int:id>/delete',methods=['POST'])
@login_required
def delete(id):
    post = Post.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()  
    flash('Post deleted successfully!','success') 
    return redirect(url_for('main.index'))      

@main.route('/post/comment/new/<int:id>', methods =  ['GET','POST'])
@login_required
def new_comment(id):
    form = CommentForm() 
    post = Post.query.filter_by(id=id).first()
    if form.validate_on_submit():
        comment = form.comment.data
        new_comment = Comment(post_comment=comment,post_id = post.id,user=current_user) 
        
        new_comment.save_comment()
        
        return redirect(url_for('.post',id = post.id))

    return render_template('new_comment.html',comment_form=form, post=post) 
     
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)    

@main.route('/user/<uname>/update',methods = ['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form=form)

   


