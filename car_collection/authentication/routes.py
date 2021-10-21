from flask import Blueprint, render_template, request, url_for, flash, redirect
from car_collection.forms import UserLoginForm
from car_collection.models import User, db, check_password_hash
from flask_login import login_user, login_required, logout_user


auth = Blueprint('auth', __name__, template_folder='auth_templates')


@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        


        new_user = User(email, password)
        db.session.add(new_user)
        db.session.commit()

        
        flash(f'You have successfully created an account under {email}', 'user-created')
        
        return redirect(url_for('site.home'))

    return render_template('sign_up.html', form = form)


@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email, password)

        logged_user = User.query.filter(User.email == email).first()
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            flash('You were successfully logged in.', 'auth-success')
            return redirect(url_for('site.home'))
        else:
            flash('Your Email/Password is incorrect', 'auth-failed')
            return redirect(url_for('auth.signin'))

    return render_template('sign_in.html', form = form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))