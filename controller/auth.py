from app import db
from flask import Flask , render_template , request , redirect , url_for , flash , abort
from validators.Auth import Login , Reqister
from flask_login import LoginManager , login_user , current_user , logout_user , login_required
from models import User



class Authentication:

    def __init__(self , *args , **kwargs):
        pass

    def SignUp(self):
        if current_user.is_authenticated:
            return redirect(url_for('main'))

        form = Reqister()
        if request.method == 'POST':
            if form.validate():
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
                    return redirect(url_for('SignUp'))
                else:
                    flash('User Exists, Please choose another email', 'error')
                    return redirect(url_for('SignUp'))
        return render_template('auth/signup.html', form=form)
    
    def SignIn(self):
        if current_user.is_authenticated:
            return redirect(url_for('main'))
        
        form = Login()
        if request.method == 'POST':
            if form.validate():
                print('Valiation Successfully')
                email = request.form.get('email')
                password = request.form.get('password')
                user = User.Users.query.filter_by(email = email).first()
                if not user:
                    flash('User Not Exist , please Try Again' ,'warning')
                    return redirect(url_for('SignIn'))
                if user and user.IsOriginalPassword(password):
                    login_user(user)
                    next_page = request.args.get('next')
                    return redirect(next_page) if next_page else redirect(url_for('main'))
        return render_template('/auth/signin.html' , form = form)
    
    def SignOut(self):
        logout_user()
        return redirect(url_for('main'))