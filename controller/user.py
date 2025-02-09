from app import db , allow_extension , app
from werkzeug.utils import secure_filename
from models import User, Order
from flask import Flask , render_template , request , redirect , url_for , flash , abort
from flask_login import LoginManager , login_user , current_user , logout_user , login_required
from validators.Auth import EditProfile , ChangePassword
import os

app=Flask(__name__)

class Account:

    def __init__(self , *args , **kwargs):
        pass

    @login_required
    def account(self):
        return render_template('/account/index.html')
    
    def account_info(self):
        return render_template('/account/info.html')
    
    def account_password(self):
        form = ChangePassword()
        if request.method == 'POST':
            if form.validate_on_submit():
                oldPassword = request.form.get('oldPassword')
                user = db.session.query(User.Users).filter_by(email = current_user.email).one()
                if not user.IsOriginalPassword(oldPassword):
                    flash('Old Password is Incorrect' , 'danger')
                    return redirect(url_for('account_password'))
                newPassword = request.form.get('newPassword')
                user.passwd = newPassword

                db.session.add(user)
                db.session.commit()
                flash('Password Changed Successfully' , 'success')
                return redirect(url_for('account_password'))
        return render_template('/account/changepassword.html' , form = form)
    
    def account_avatar(self):
        if request.method == 'POST' and 'avatar' in request.files:
            avatar = request.files['avatar']
            filename = avatar.filename
            fileSecure = secure_filename(filename)
            if not allow_extension(filename):
                flash('Extension File is Not Allowed' , 'danger')
                return redirect(url_for('account_avatar'))
            file_path = os.path.join(app.config['UPLOAD_DIR'] , fileSecure)
            avatar.save(file_path)
            user = db.session.query(User.Users).filter_by(email = current_user.email).one()
            user.avatar = f'uploads/{filename}'
            db.session.add(user)
            db.session.commit()
            flash('Uploaded Picture Successfully' , 'success')
            return redirect(url_for('account_avatar'))
        return render_template('/account/avatar.html')
    
    def account_edit(self):
        form = EditProfile()
        if request.method == 'POST':
            if form.validate_on_submit():
                name = request.form.get('name')
                email = request.form.get('email')
                phone = request.form.get('phone')
                user = db.session.query(User.Users).filter_by(email = current_user.email).one()
                # Updating Profile Account
                user.name = name
                user.email = email
                user.phone = phone
                # Add And Commit
                db.session.add(user)
                db.session.commit()

                return redirect(url_for('account_info'))
            
        return render_template('/account/edit.html' , form = form)


    @login_required
    def orders(self):
        # گرفتن تمام سفارشات کاربر
        orders = Order.query.filter_by(user_id=current_user.id).all()
        return render_template('account/orders.html', orders=orders)
    
    @login_required
    def order_detail(self, order_id):
        # گرفتن جزئیات سفارش
        order = Order.query.get_or_404(order_id)
        return render_template('account/order_detail.html', order=order)