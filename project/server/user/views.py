# project/server/user/views.py


#############
#  imports  #
#############

import sqlalchemy
from flask import render_template, Blueprint, url_for, \
    redirect, request, flash
from flask.ext.login import login_user, logout_user, login_required, \
    current_user

from project.server import db, bcrypt
from project.server.models import User
from project.server.user.forms import RegisterForm, LoginForm


############
#  config  #
############

user_blueprint = Blueprint('user', __name__,)


############
#  routes  #
############

@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        email = User.query.filter_by(email=form.email.data).first()
        username = User.query.filter_by(
            username=form.username.data).first()
        if email is not None:
            flash('Email must be unique.', 'danger')
            return redirect(url_for('user.register'))
        if username is not None:
            flash('Username must be unique.', 'danger')
            return redirect(url_for('user.register'))
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data
        )
        try:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Thank you for registering.', 'success')
        except sqlalchemy.exc.IntegrityError as err:
            print('Handle Error:{0}'.format(err))
            flash('Something terrible happened.', 'danger')
        return redirect(url_for('user.register'))
        flash('Thank you for registering.', 'success')
    return render_template('user/register.html', form=form)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                user.password, request.form['password']):
            login_user(user)
            flash('You are logged in. Welcome!', 'success')
            return redirect(url_for('user.account', id=user.id))
        else:
            flash('Invalid email and/or password.', 'danger')
    return render_template('user/login.html', form=form)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out. Bye!', 'success')
    return redirect(url_for('user.login'))


@user_blueprint.route('/profile/<id>')
@login_required
def account(id):
    user = User.query.filter_by(id=id).first()
    if not user or current_user.id is not user.id:
        flash('You are not authorized to access that page.', 'danger')
        return redirect(url_for('user.account', id=current_user.id))
    else:
        return render_template('user/account.html', user=user)
