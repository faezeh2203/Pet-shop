from app import db , allow_extension , app
from werkzeug.utils import secure_filename
from models import User
from flask import Flask , render_template , request , redirect , url_for , flash , abort
from flask_login import LoginManager , login_user , current_user , logout_user , login_required
from validators.Auth import EditProfile , ChangePassword
from validators.Admin import CreateUser , EditUser
import os

app=Flask(__name__)

class Admin:

    def __init__(self , *args , **kwargs):
        pass

    @login_required
    def index(self):
        if not current_user.admin:
            return redirect(url_for('account'))
        
        return render_template('/admin/index.html')
    
    def admin_account_info(self):
        return render_template('/admin/info.html')
    
    def admin_account_password(self):
        form = ChangePassword()
        if request.method == 'POST':
            if form.validate_on_submit():
                oldPassword = request.form.get('oldPassword')
                user = db.session.query(User.Users).filter_by(email = current_user.email).one()
                if not user.IsOriginalPassword(oldPassword):
                    flash('Old Password is Incorrect' , 'danger')
                    return redirect(url_for('admin_account_password'))
                newPassword = request.form.get('newPassword')
                user.passwd = newPassword

                db.session.add(user)
                db.session.commit()
                flash('Password Changed Successfully' , 'success')
                return redirect(url_for('admin_account_password'))
        return render_template('/admin/changepassword.html' , form = form)
    
    def admin_account_avatar(self):
        if request.method == 'POST' and 'avatar' in request.files:
            avatar = request.files['avatar']
            filename = avatar.filename
            fileSecure = secure_filename(filename)
            if not allow_extension(filename):
                flash('Extension File is Not Allowed' , 'danger')
                return redirect(url_for('admin_account_avatar'))
            file_path = os.path.join(app.config['UPLOAD_DIR' , ''], fileSecure)
            avatar.save(file_path)
            user = db.session.query(User.Users).filter_by(email = current_user.email).one()
            user.avatar = f'uploads/{filename}'
            db.session.add(user)
            db.session.commit()
            flash('Uploaded Picture Successfully' , 'success')
            return redirect(url_for('admin_account_avatar'))
        return render_template('/admin/avatar.html')
    
    def admin_account_edit(self):
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

                return redirect(url_for('admin_account_info'))
            
        return render_template('/admin/edit.html' , form = form)
    
    def get_all_users(self):
        get_all_user = User.Users.query.all()
        return render_template('/admin/user/list.html' , users = get_all_user)
    
    def create_user(self):
        form = CreateUser()
        if request.method == 'POST':
            if form.validate_on_submit():
                name = request.form.get('name')
                email = request.form.get('email')
                password = request.form.get('password')
                name = request.form['name']
                email = request.form['email']
                password = request.form['password']  # رمز عادی دریافت‌شده از فرم
                user = User.Users.query.filter_by(email=email).first()
                if not user:
                    newUser = User.Users(name=name, email=email)
                    newUser.passwd = password  # رمز عادی به setter ارسال می‌شود
                    db.session.add(newUser)
                    db.session.commit()  # رمز هش‌شده ذخیره می‌شود
                    flash('User Created Successfully', 'success')
                    return redirect(url_for('create_user'))
                else:
                    flash('User Exists, Please choose another email', 'error')
                    return redirect(url_for('create_user'))
        return render_template('/admin/user/create.html' , form = form)
    
    def edit_user(self):
        form = EditUser()
        user = db.session.query(User.Users).filter_by(id = request.args.get('id')).one()
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            
            user.name = name
            user.email = email
            user.phone = phone

            db.session.add(user)
            db.session.commit()
            return redirect(url_for('get_all_users'))
        return render_template('/admin/user/edit.html' , form = form , user = user)