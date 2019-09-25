from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import ValidationError, DataRequired, EqualTo
import datetime
from datetime import timedelta

class RatesForm(FlaskForm):
    today = datetime.datetime.today()
    week_before = today-timedelta(days=7)
    for_date = DateField('Date', validators=[DataRequired()], format="%Y-%m-%d", default=week_before)
    to_date = DateField('To Date', format="%Y-%m-%d", default=today)
    submit = SubmitField('Get Rates')
