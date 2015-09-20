from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, RadioField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from app import app, db, models
from models import Poll, Choice

class NewPollForm(Form):
    title = StringField(validators=[DataRequired()])
    detail = TextAreaField('detail', validators=[DataRequired()])
    choice = StringField('choice', validators=[DataRequired()])
    choice2 = StringField('choice')
    choice3 = StringField('choice')
    choice4 = StringField('choice')
    choice5 = StringField('choice')
    deadline = DateField('deadline', validators=[DataRequired()])
    equality = RadioField('equality', choices=[('yes','One Vote for Each'),('no','Respect to Ability')])
    individual = RadioField('individual', choices=[('yes','Individual'),('no','Group')])
    remember_me = BooleanField('remember_me', default=False)

class JoinGroupForm(Form):
	number = IntegerField('number', validators=[DataRequired()])

class GroupVoteForm(Form):
	possibilities = RadioField('possible', validators=[DataRequired()])

def generate_form(poll):
	form = GroupVoteForm()
	if poll.choices is not None:
		form.possibilities.choices = [(item.id, item.content)
        for item in poll.choices]
	return form