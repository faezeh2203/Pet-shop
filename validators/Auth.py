from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class Login(FlaskForm):
    email = StringField(
        label='Email',
        validators=[
            DataRequired('Email Field is Required'),
            Email('Email is Invalid')
        ]
    )
    
    password = PasswordField(
        label='Password',
        validators=[
            DataRequired('Password Field Is Required!'),
            Length(min=8, message='Password Is Less Than 8 Characters')
        ]
    )
    submit = SubmitField(label='Login')


class Reqister(FlaskForm):
    name = StringField(
        label='Name',
        validators=[DataRequired('Name Field is Required')]
    )
    email = StringField(
        label='Email',
        validators=[
            DataRequired('Email Field is Required'),
            Email('Email is Invalid')
        ]
    )
    password = PasswordField(
        label='Password',
        validators=[
            DataRequired('Password Field Is Required!'),
            Length(min=8, message='Password Is Less Than 8 Characters')
        ]
    )
    confirm = PasswordField(
        label='Confirm Password',
        validators=[
            DataRequired('Conferm Password Field Is Required!'),
            Length(min=8, message='Password Is Less Than 8 Characters'),
            EqualTo('password', message='Confirm Does Not Match With Password')
        ]
    )
    submit = SubmitField(label='Register')


class EditProfile(FlaskForm):

    name = StringField(
        label='Name',
        validators=[DataRequired('Name Field is Required')]
    )
    email = StringField(
        label='Email',
        validators=[
            DataRequired('Email Field is Required'),
            Email('Email is Invalid')
        ]
    )
    phone = StringField(
        label='phone',
        validators=[DataRequired('phone Field is Required')]
    )

    submit = SubmitField('Update Profile')


class ChangePassword(FlaskForm):
    oldPassword = PasswordField(
            label='oldpassword',
            validators=[
                DataRequired('Old Password Field Is Required!'),
                Length(min=8, message='Password Is Less Than 8 Characters')
            ]
        )
    
    newPassword = PasswordField(
            label='newpassword',
            validators=[
                DataRequired('New Password Field Is Required!'),
                Length(min=8, message='Password Is Less Than 8 Characters')
            ]
        )
    
    confirm = PasswordField(
        label='Confirm Password',
        validators=[
            DataRequired('Conferm Password Field Is Required!'),
            Length(min=8, message='Password Is Less Than 8 Characters'),
            EqualTo('newPassword', message='Confirm Does Not Match With Password')
        ]
    )

    submit = SubmitField('Change Password')