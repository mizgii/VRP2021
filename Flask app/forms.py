from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField


class SimForm(FlaskForm):
    points = IntegerField(label='Number of points except depot (even, max 50)')
    number_vehicles = IntegerField(label='Number of vehicles (recommended between 2 and 7)')
    capacity = IntegerField(label='Capacity of each vehicle')
    submit = SubmitField(label='Start')