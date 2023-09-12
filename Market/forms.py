from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,IntegerField
from wtforms.validators import Length,EqualTo,Email,DataRequired,ValidationError
from Market.models import User
class RegisterForm(FlaskForm):
    def validate_username(self,username_to_check):
        user=User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already existe, Please try a different username')
    def validate_emailaddress(self,email_to_check):
        email=User.query.filter_by(emailaddress=email_to_check.data).first()
        if email:
            raise ValidationError('emailaddress already exits, Please try a different emailaddress')
    username=StringField(label='User Name:', validators=[Length(min=2,max=30),DataRequired()])
    emailaddress=StringField(label='Email Address',validators=[Email(),DataRequired()])
    password1=PasswordField(label='Password', validators=[Length(min=6),DataRequired()])
    password2=PasswordField(label='Confirm Password',validators=[EqualTo('password1'),DataRequired()])
    submit=SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username=StringField(label='User Name: ',validators=[DataRequired()])
    password=PasswordField(label='Password: ',validators=[DataRequired()])
    submit=SubmitField(label='Sign in')

class AdditemForm(FlaskForm):
    name=StringField(label='Item name :')
    price=IntegerField(label='Price :')
    barcode=StringField(label='Barcode : ')
    description=StringField(label='Description :')
    submit=SubmitField(label='Add item')

class PurchaseItemForm(FlaskForm):
    submit=SubmitField(label='Purchase Item!')

class SellItemForm(FlaskForm):
    submit=SubmitField(label='Sell Item!')

