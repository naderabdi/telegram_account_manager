from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class AddAccountForm(FlaskForm):
    phone_number = StringField("Phone Number", validators=[DataRequired()])
    api_id = StringField("API ID", validators=[DataRequired()])
    api_hash = StringField("API Hash", validators=[DataRequired()])
    submit = SubmitField("Add Account")

class SwitchAccountForm(FlaskForm):
    account_id = IntegerField("Account ID", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Switch Account")

class SendMessageForm(FlaskForm):
    telegram_id = StringField("Telegram ID", validators=[DataRequired()])
    message = StringField("Message", validators=[DataRequired()])
    submit = SubmitField("Send Message")
