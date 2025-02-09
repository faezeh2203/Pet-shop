from flask import Flask, render_template, request, redirect, url_for, flash, abort
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user ,current_user ,logout_user ,login_required
import os
from flask_login import login_required, current_user

# ایجاد و پیکربندی برنامه
app = Flask(__name__)

# تنظیمات امنیتی و مسیرهای آپلود
app.secret_key = 'e033dd67b1b6314a8fa42806e268382f'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'static', 'uploads')

def allow_extension(filename):
    ext = filename.split('.')[-1].lower()
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    return ext in allowed_extensions

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_DIR'] = UPLOAD_DIR

# مقداردهی اولیه پایگاه داده
db = SQLAlchemy(app)

# مقداردهی اولیه مدیریت لاگین
login=LoginManager()
login.login_view = 'SignIn'
login.login_message_category = 'info'
login.init_app(app)

# Import Models
from models import User, Product, Order, OrderProduct, Cart, CartItem

# Import Controller
from controller import home , user , auth , admin, cart

homeController = home.Home()
userController = user.Account()
authController = auth.Authentication()
adminController = admin.Admin()
cartController = cart.Cart()

@login.user_loader
def userLoader(user_id):
    return User.Users.query.get(user_id)

# Route Home
app.add_url_rule('/', 'main', homeController.main)

# Route Account User
app.add_url_rule('/account', 'account', userController.account)
app.add_url_rule('/account/info', 'account_info', userController.account_info)
app.add_url_rule('/account/changepassword', 'account_password', userController.account_password, methods=['GET', 'POST'])
app.add_url_rule('/account/avatar', 'account_avatar', userController.account_avatar, methods=['GET', 'POST'])
app.add_url_rule('/account/edit', 'account_edit', userController.account_edit, methods=['GET', 'POST'])

# Route Authentication
app.add_url_rule('/signout', 'SignOut', authController.SignOut, methods=['GET', 'POST'])
app.add_url_rule('/signup', 'SignUp', authController.SignUp, methods=['GET', 'POST'])
app.add_url_rule('/signin', 'SignIn', authController.SignIn, methods=['GET', 'POST'])

# Route Admin
app.add_url_rule('/admin', 'index', adminController.index)
app.add_url_rule('/admin/user', 'get_all_users', adminController.get_all_users)
app.add_url_rule('/admin/user/create', 'create_user', adminController.create_user, methods=['GET', 'POST'])
app.add_url_rule('/admin/user/edit', 'edit_user', adminController.edit_user, methods=['GET', 'POST'])
app.add_url_rule('/admin/info', 'admin_account_info', adminController.admin_account_info)
app.add_url_rule('/admin/edit', 'admin_account_edit', adminController.admin_account_edit, methods=['GET', 'POST'])
app.add_url_rule('/admin/changepassword', 'admin_account_password', adminController.admin_account_password, methods=['GET', 'POST'])
app.add_url_rule('/admin/avatar', 'admin_account_avatar', adminController.admin_account_avatar, methods=['GET', 'POST'])


# Route Cart
app.add_url_rule('/account/cart', 'cart', cartController.cart)
app.add_url_rule('/account/cart/add/<int:product_id>', 'add_to_cart', cartController.add_to_cart)
app.add_url_rule('/account/cart/remove/<int:cart_id>', 'remove_from_cart', cartController.remove_from_cart)
app.add_url_rule('/account/cart/update/<int:cart_id>/<int:quantity>', 'update_cart', cartController.update_cart)

# Route Order (برای ثبت سفارشات و نمایش آن‌ها)
app.add_url_rule('/account/orders', 'orders', userController.orders)
app.add_url_rule('/account/order/<int:order_id>', 'order_detail', userController.order_detail)


if __name__ == '__main__':
    app.run(port=8080, debug=True)
