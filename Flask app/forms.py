from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField


class SimForm(FlaskForm):
    points = IntegerField(label='Number of points except depot (even, max 50)',validators=[DataRequired()])
    number_vehicles = IntegerField(label='Number of vehicles (recommended between 2 and 7)',validators=[DataRequired()])
    capacity = IntegerField(label='Capacity of each vehicle',validators=[DataRequired()])
    tlimit = IntegerField(label='Solution search time limit (seconds)',validators=[DataRequired()])
    submit = SubmitField(label='Start')
