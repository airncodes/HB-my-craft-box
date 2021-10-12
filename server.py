from flask import Flask, render_template, request, flash, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from model import connect_to_db
import crud
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "nopeeks"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def show_homepage():
    """Shows the homepage"""
    return render_template("homepage.html")

@app.route('/signup')
def show_signup():
    """Shows the signup page"""
    return render_template("signup.html")

@app.route('/signup', methods=['POST'])
def sign_up():
    """User sign up"""
    
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    user_name = request.form.get('user_name')
    email = request.form.get('email')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    
    user = crud.find_user_by_email(email)
    if user:
        flash('Cannot create an account with that email. Try again.')
        return redirect('/signup')
        
    if password == password2:
        password_hash = generate_password_hash(password)
        crud.create_user(fname, lname, user_name, email, password_hash)
        flash('Account created! Please log in.')
        return redirect('/')
    else:
        flash('Passwords must match')
        return redirect('/signup')
        
    
@app.route('/login')
def show_login():
    """Shows the signup page"""
    return render_template("login.html")    

@app.route('/login', methods=['POST'])
def login_user():
    """Login page for the user"""
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.find_user_by_email(email)
    
 
    if not user:
        flash('Email not recognized. Try again.')
        return redirect('/login')
    
    passwordcheck = crud.check_password(user, password)
    if not passwordcheck:
        flash('Invalid password. Try again.')
        return redirect('/login')
        
    else:
        flash(f'Logged in {user.fname}')
        return render_template("craftbox.html")





@app.route('/account')
def show_account_page():
    """Shows user's account page"""
    pass

@app.route('/logout')
def logout_user():
    """Logs out for the user"""
    pass

@app.route('/search')
def user_search():
    """Shows user search results based on their query"""
    pass

@app.route('/selection')
def show_selected_item():
    """Shows page for the selected item"""
    pass

@app.route('/addlink', methods=['POST'])
def add_link():
    """Allows a user to add a link"""

    name = request.form.get('name')
    link_path = request.form.get('link_path')
    image = request.form.get('image')
    notes = request.form.get('notes')

    user_id = crud.get_userid_by_email(email)
    
    crud.add_link(name, link_path, user_id, image=None, notes=None)
    flash('Link Added!')

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)