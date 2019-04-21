from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired

class AddDomainForm(FlaskForm):
    domain = StringField('domain', validators=[DataRequired()])
    submit = SubmitField('Add')

class RemoveDomainForm(FlaskForm):
    domain = HiddenField('domain')
    submit = SubmitField('Remove')
