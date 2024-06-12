from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, DateTimeField, FloatField, SelectField
from wtforms.validators import DataRequired, EqualTo

from models import Car


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SignUpForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')


class CarForm(FlaskForm):
    make = StringField('Make', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AppointmentForm(FlaskForm):
    car_id = IntegerField('Car ID', validators=[DataRequired()])
    service_id = IntegerField('Service ID', validators=[DataRequired()])
    appointment_date = DateTimeField('Appointment Date', validators=[DataRequired()])
    submit = SubmitField('Book Appointment')


class ServiceForm(FlaskForm):
    name = StringField('Service Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    cost = FloatField('Estimated Cost', validators=[DataRequired()])
    car_id = SelectField('Car', coerce=int)
    submit = SubmitField('Add Service')

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.car_id.choices = [(car.id, car.make) for car in Car.query.all()]
