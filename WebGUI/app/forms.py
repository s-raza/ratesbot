from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import ValidationError, DataRequired, EqualTo

class RatesForm(FlaskForm):
    for_date = DateField('Date', validators=[DataRequired()], format="%Y-%m-%d")
    submit = SubmitField('Get Rates')
