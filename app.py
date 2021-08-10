from forms import LoginForm, RegistrationForm, FeedBackForm
from flask import Flask,redirect,render_template,session
from models import Feedback, db,connect_db,User
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY',"secretisthis")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',"postgresql:///feedback")

connect_db(app)


@app.route('/')
def home_page():
    return redirect('/login')

@app.route('/register', methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,password=form.password.data,email=form.email.data,first_name=form.first_name.data,last_name=form.last_name.data).register()

        session['username'] = new_user.username
        return redirect(f'/users/{new_user.username}')
    return render_template('register.html',form=form)


@app.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.username.data)
        if user.authenticate(form.password.data):
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/users/<username>')
def user_page(username):
    user = User.query.get_or_404(username)
    if session.get('username')==user.username:
        return render_template('user.html',user=user)
    else:
        return "No"

@app.route('/users/<username>/delete',methods=["POST"])
def delete(username):
    user = User.query.get_or_404(username)
    if session.get('username')==user.username:
        db.session.delete(user)
        db.session.commit()

    return redirect('/')


@app.route('/users/<username>/feedback/add',methods=["GET","POST"])
def add_feedback(username):
    form = FeedBackForm()
    user = User.query.get_or_404(username)

    if form.validate_on_submit() and session.get('username')==user.username:
        feedback = Feedback(title=form.title.data,content=form.content.data,username=user.username)
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{username}')

    return render_template('feedback.html',form = form,user = user)

@app.route('/feedback/<feedback_id>/update',methods=["GET","POST"])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    
    user = User.query.get_or_404(feedback.user.username)
  
    form = FeedBackForm()
    input_title = form.title.data
    input_content = form.content.data
    if session.get('username')==user.username:
        form.title.data=feedback.title
        form.content.data=feedback.content

    if form.validate_on_submit():
        feedback.title = input_title
        feedback.content = input_content

        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{user.username}')

    return render_template('update_feedback.html',form=form,feedback=feedback)

@app.route('/feedback/<feedback_id>/delete',methods=["POST"])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    
    user = User.query.get_or_404(feedback.user.username)
    if session.get('username')==user.username:
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f'/users/{feedback.user.username}')