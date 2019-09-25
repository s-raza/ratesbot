from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import ValidationError, DataRequired, EqualTo
import datetime
from datetime import timedelta

class RatesForm(FlaskForm):
    today = datetime.datetime.today()
    week_before = today-timedelta(days=7)
    two_weeks_before = today-timedelta(days=14)
    days30_before = today-timedelta(days=30)
    days45_before = today-timedelta(days=45)
    days60_before = today-timedelta(days=60)
    for_date = DateField('Date', validators=[DataRequired()], format="%Y-%m-%d", default=week_before)
    to_date = DateField('To Date', format="%Y-%m-%d", default=today)
    submit = SubmitField('Get Rates')
    last_1_week = SubmitField('Last 1 week')
    last_2_weeks = SubmitField('Last 2 weeks')
    last_30_days = SubmitField('Last 30 days')
    last_45_days = SubmitField('Last 45 days')
    last_60_days = SubmitField('Last 60 days')
