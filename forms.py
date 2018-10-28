from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from model import Industry, Company, Salary, Interest


# class IndustryForm(FlaskForm):
#     """Select the company and period want to show."""

#     choices = []
#     for industry in Industry.query.all():
#       choices.append((industry.name, industry.name))

#     industry = SelectField("Industry", 
#                           choices=choices, 
#                           validators=[DataRequired()])
    
#     view = SubmitField('Create the view')


class CompanyForm(FlaskForm):
    """Select the company and period want to show."""

    company = StringField('Company', validators=[DataRequired()], 
                                     render_kw={"placeholder": "Company Name"})


# class IndustryForm(FlaskForm):
#     """Select the company and period want to show."""

#     choices = []
#     for industry in Industry.query.all():
#       choices.append((industry.name, industry.name))

#     industry = SelectField("Industry", 
#                           choices=choices, 
#                           validators=[DataRequired()])
    
#     view = SubmitField('Create the view')



# class RegisterForm(FlaskForm):
#     """User registration form."""

#     name = StringField("Name", validators=[DataRequired()])
#     email = StringField("E-mail", validators=[DataRequired(), Email()])
#     password = PasswordField("Password", validators=[DataRequired(),
#                                                      Length(min=8,
#                                                             message=SMALL_PASSWORD_MESSAGE)])
#     repeat_password = PasswordField('Repeat Password',
#                                     validators=[DataRequired(), EqualTo('password')])

#     register = SubmitField("Register")


# class LoginForm(FlaskForm):
#     """User login form."""

#     email = StringField("E-mail", validators=[DataRequired(), Email()])
#     password = PasswordField("Password", validators=[DataRequired()])
#     login = SubmitField("Login")