from datetime import datetime
from flask import render_template, flash, redirect, url_for, session, request

from models import User, db, Car, Appointment, Service
from forms import SignUpForm, LoginForm, ChangePasswordForm, CarForm, AppointmentForm, ServiceForm
from utils import create_user, check_user


def all_my_routes(app):
    @app.route('/')
    def home() -> str:
        return render_template('home.html', year=datetime.now().year)

    @app.route('/about')
    def about() -> str:
        return render_template('about.html', year=datetime.now().year)

    @app.route('/services', methods=['GET', 'POST'])
    def services():
        form = ServiceForm()
        services_all = Service.query.all()
        if form.validate_on_submit():
            car = Car.query.get(form.car_id.data)
            if car:
                new_service = Service(name=form.name.data, description=form.description.data, cost=form.cost.data,
                                      car_id=car.id)
                db.session.add(new_service)
                db.session.commit()
                flash('Service added successfully.')
                return redirect(url_for('services'))
            else:
                flash('No car found with the given id.')
        return render_template('services.html', form=form, services=services_all)

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        form = SignUpForm()
        if form.validate_on_submit():
            user_created = create_user(form.name.data, form.username.data, form.email.data, form.password.data,
                                       form.phone_number.data)
            if user_created:
                flash('Account created successfully.')
                return redirect(url_for('login'))
            else:
                flash('A user with that username already exists.')
        return render_template('signup.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user_exists = check_user(form.username.data, form.password.data)
            if user_exists:
                session['logged_in'] = True
                session['username'] = form.username.data
                session['user_id'] = user_exists.id
                flash('Logged in successfully.')
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password.')
        return render_template('login.html', form=form)

    @app.route('/logout')
    def logout():
        session.clear()
        flash('You have been logged out.')
        return redirect(url_for('home'))

    @app.route('/profile', methods=['GET', 'POST'])
    def profile():
        if session.get('logged_in'):
            user = User.query.filter_by(username=session['username']).first()
            form = SignUpForm(obj=user)
            password_form = ChangePasswordForm()
            if 'submit' in request.form and form.validate_on_submit():
                user.name = form.name.data
                user.username = form.username.data
                user.email = form.email.data
                user.phone_number = form.phone_number.data
                db.session.commit()
                flash('Profile updated successfully.')
                return redirect(url_for('profile'))
            elif 'change_password' in request.form and password_form.validate_on_submit():
                if user.check_password(password_form.old_password.data):
                    if password_form.new_password.data == password_form.confirm_password.data:
                        user.set_password(password_form.new_password.data)
                        db.session.commit()
                        flash('Password changed successfully.')
                        return redirect(url_for('profile'))
                    else:
                        flash('New password and confirm new password do not match.')
                else:
                    flash('Incorrect old password.')
            return render_template('profile.html', form=form, user=user, password_form=password_form)
        else:
            flash('You must be logged in to view this page.')
            return redirect(url_for('login'))

    @app.route('/mycars', methods=['GET', 'POST'])
    def mycars():
        if 'username' not in session:
            flash('You must be logged in to view this page.')
            return redirect(url_for('login'))

        user = User.query.filter_by(username=session['username']).first()

        if user is None:
            flash('Invalid user.')
            return redirect(url_for('login'))

        cars = Car.query.filter_by(user_id=user.id).all()
        form = CarForm()
        if form.validate_on_submit():
            new_car = Car(make=form.make.data, model=form.model.data, year=form.year.data,
                          user_id=user.id)
            db.session.add(new_car)
            db.session.commit()
            flash('Car added successfully.')
            return redirect(url_for('mycars'))
        return render_template('mycars.html', year=datetime.now().year, cars=cars, form=form)

    @app.route('/mycars/update/<int:car_id>', methods=['GET', 'POST'])
    def update_car(car_id):
        car = Car.query.get_or_404(car_id)
        form = CarForm(obj=car)
        if form.validate_on_submit():
            car.make = form.make.data
            car.model = form.model.data
            car.year = form.year.data
            db.session.commit()
            flash('Car updated successfully.')
            return redirect(url_for('mycars'))
        cars = Car.query.all()
        return render_template('mycars.html', form=form, cars=cars)

    @app.route('/mycars/delete/<int:car_id>', methods=['POST'])
    def delete_car(car_id):
        car = Car.query.get_or_404(car_id)
        db.session.delete(car)
        db.session.commit()
        flash('Car deleted successfully.')
        return redirect(url_for('mycars'))

    @app.route('/book_appointment', methods=['GET', 'POST'])
    def book_appointment():
        form = AppointmentForm()
        if form.validate_on_submit():
            appointment = Appointment(user_id=session['user_id'], car_id=form.car_id.data,
                                      service_id=form.service_id.data, appointment_date=form.appointment_date.data)
            db.session.add(appointment)
            db.session.commit()
            flash('Appointment booked successfully.')
            return redirect(url_for('home'))
        return render_template('book_appointment.html', form=form)
