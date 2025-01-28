from flask import Flask , render_template , request , redirect , url_for , flash , abort
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from validators.Auth import Login , Reqister , EditProfile , ChangePassword
from flask_login import LoginManager , login_user , current_user , logout_user , login_required
import os

app=Flask(__name__)

app.secret_key='e033dd67b1b6314a8fa42806e268382f'

# UPLOAD_DIR = os.path.curdir + '/static/uploads/'
BASE_DIR=os.path.abspath(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'static', 'uploads')

def allow_extension(filename):
    ext = filename.split('.')[-1].lower()
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    return ext in allowed_extensions


app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(BASE_DIR,'blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_DIR'] = UPLOAD_DIR

login=LoginManager()
login.login_view = 'SignIn'
login.login_message_category = 'info'
login.init_app(app)

db=SQLAlchemy(app)

from models import User
from models import Product , Order , OrderProduct
from controller import home , user , auth


homeController = home.Home()
userController = user.Account()
authController = auth.Authentication()

@login.user_loader
def userLoader(user_id):
    return User.Users.query.get(user_id)

#Route Home
app.add_url_rule('/' , 'main' , homeController.main)

#Route Account User
app.add_url_rule('/account' , 'account' , userController.account)
app.add_url_rule('/account/info' , 'account_info' , userController.account_info)
app.add_url_rule('/account/chengepassword' , 'account_password' , userController.account_password , methods = ['get' , 'post'])
app.add_url_rule('/account/avatar' , 'account_avatar' , userController.account_avatar , methods = ['get' , 'post'])
app.add_url_rule('/account/edit' , 'account_edit' , userController.account_edit , methods = ['get' , 'post'])

#Route Authentication
app.add_url_rule('/signout' , 'SignOut' , authController.SignOut , methods = ['get' , 'post'])
app.add_url_rule('/signup' , 'SignUp' , authController.SignUp , methods = ['get' , 'post'])
app.add_url_rule('/signin' , 'SignIn' , authController.SignIn , methods = ['get' , 'post'])



if __name__=='__main__':
    app.run(port=8080,debug=True)



