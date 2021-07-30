from flask_login.config import EXEMPT_METHODS
from flaskblog.forms import LoginForm, RegisterForm, ContactForm, UpdateAccountForm
from flaskblog import app, db, bcrypt, login_manager
from flask.helpers import flash, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flaskblog.models import User, Contact
from flask_mail import Mail
from flask import Flask, render_template, redirect, request, abort
import os



@login_manager.user_loader
def load_user(id):
    return User.query.get(id)



@app.route("/")
def index():
    contacts = Contact.query.order_by(Contact.data_created).all()
    return render_template('index.html', contacts=contacts)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next = request.args.get('next')
            return redirect(next) if next else redirect("/")
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', form=form)



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect('/login')

    return render_template('register.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, number=form.number.data, user_id=current_user.id)
        db.session.add(contact)
        db.session.commit()
        flash('Contact created successfully', 'success')
        return redirect("/")

    return render_template('dashboard.html', form=form)



@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = UpdateAccountForm()
    contact = Contact.query.filter_by(id=id).first()
    if current_user.id != contact.owner.id:
        abort(403)
    else:
        if form.validate_on_submit():
            contact.first_name = form.first_name.data
            contact.last_name = form.last_name.data
            contact.email = form.email.data
            contact.number = form.number.data
            db.session.commit()
            flash('Your contact has been updated.', 'info')
            return redirect("/")
        elif request.method == 'GET':
            form.first_name.data = contact.first_name
            form.last_name.data = contact.last_name
            form.email.data = contact.email
            form.number.data = contact.number

    return render_template("update.html", form=form)



@app.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    contact = Contact.query.filter_by(id=id).first()
    if current_user.id != contact.owner.id:
        abort(403)
    else:
        db.session.delete(contact)
        db.session.commit()
        flash('Your contact has been deleted.', 'info')
        return redirect("/")
