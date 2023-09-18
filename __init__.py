from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
UPLOAD_FOLDER = 'blogproject/static/profile_pics/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data1.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app,db)

login_manager = LoginManager()

# We can now pass in our app to the login manager
login_manager.init_app(app)

login_manager.login_view = "login"

from flask import Flask , render_template, request, url_for, redirect
from flask_login import login_user, current_user, logout_user, login_required
from blogproject.forms import LoginForm, RegisterForm, BlogForm, AccountForm
from blogproject import db
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from blogproject.models import User, BlogPost
from flask import send_from_directory

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', methods =['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user1= User.query.filter_by(email=form.email.data).first()
        user2=user1.check_password(form.password.data)
        if user1 and user2 is not None:
            login_user(user1)
            return redirect(url_for('index'))
    return render_template('login.html',form=form)


@app.route('/register', methods=['POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        user = User(email,username,password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html',form=form)


@app.route('/welcome',methods=['POST'])
@login_required
def welcome():
    user2=user1.name
    return render_template('welcome.html',user2=user2)


@app.route('/create_blogpost',methods=['POST'])
@login_required
def blogpost():
    form = BlogForm()
    if form.validate_on_submit():
        title = form.title.data
        blog = form.blog.data
        now = datetime.now()
        user_id=current_user.id
        x = datetime.now()
        current_date = x.strftime("%x")
        current_time = now.strftime("%H:%M:%S")
        blog1 = BlogPost(title,blog,current_date,current_time,user_id)
        db.session.add(blog1)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('post.html',form=form)

@app.route('/api/blogpost/<int:post_id>', methods=['PUT', 'PATCH'])
@login_required
def update_blogpost(post_id):
    # Find the blog post by its ID
    blog_post = BlogPost.query.get(post_id)

    if blog_post is None:
        return jsonify({'message': 'Blog post not found'}), 404
    if blog_post.user_id != current_user:
        return jsonify({'message': 'Unauthorized'}), 403
    data = request.json  
    if 'title' in data:
        blog_post.title = data['title']
    if 'blog' in data:
        blog_post.blog = data['blog']
    # Commit the changes to the database
    db.session.commit()
    return jsonify({'message': 'Blog post updated successfully'})

@app.route('/api/blogpost/<int:post_id>', methods=['DELETE'])
@login_required
def delete_blogpost(post_id): 
    blog_post = BlogPost.query.get(post_id)
    if blog_post is None:
        return jsonify({'message': 'Blog post not found'}), 404
    if blog_post.user_id != current_user:
        return jsonify({'message': 'Unauthorized'}), 403
    # Delete the blog post
    db.session.delete(blog_post)
    db.session.commit()
    return jsonify({'message': 'Blog post deleted successfully'})

@app.route('/posts',methods=['GET'])
def read_others_title():
    user_title = BlogPost.query.with_entities(BlogPost.title)
    blog5 = BlogPost.query.all()

    lst = []
    for titles in user_title:
        for item in titles:
            lst.append(item)
            count= 0

        for user in blog:
            current_user= user.current_date

            if count == 0:
                if current_user not in lst:
                    lst.append(current_user)
                    count= count+ 1
    count2= 1
    return render_template('read_posts.html', lst=lst, count2=1)

@app.route('/read_blog/<titles>',methods=['GET'])
def read_blog(titles):
    user_blog=BlogPost.query.filter_by(title=titles).first()
    user_post=user_blog.blog
    return render_template('user_blog.html',user_post=user_post)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/update_account',methods=['PUT'])
@login_required
def account():
    user_image= User.query.filter_by(email=current_user.email).first()
    filename=user_image.profile_pics
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            current_user.profile_pics=filename
            db.session.commit()
    form=AccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
    return render_template('picture.html',form=form,filename=filename)

db.create_all()
