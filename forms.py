from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CompanyForm(FlaskForm):
    """Select the company and period want to show."""

    company = StringField('Company', validators=[DataRequired()], 
                                     render_kw={"placeholder": "Company Name"})

