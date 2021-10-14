from flask import Flask, render_template, request, flash, session, redirect
from flask_login import login_required, current_user, login_user, logout_user
from model import connect_to_db, login_manager
import crud
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "nopeeks"
app.jinja_env.undefined = StrictUndefined

login_manager.init_app(app)
login_manager.login_view = 'craftbox'


@app.route('/')
def show_homepage():
    """Shows the homepage"""
    return render_template("homepage.html")


@app.route('/signup')
def show_signup():
    """Shows the signup page"""
    return render_template("signup.html")

@app.route('/signup', methods=['POST', 'GET'])
def sign_up():
    """User sign up"""
    
    if current_user.is_authenticated:
        return redirect('/craftbox.html')
    
    if request.method == "POST":
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
            password_hash = crud.set_password(user, password)
            crud.create_user(fname, lname, user_name, email, password_hash)
            flash('Account created! Please log in.')
            return redirect('/')
        else:
            flash('Passwords must match')
            return redirect('/signup')
    return redirect('/signup')


@app.route('/craftbox')
@login_required
def show_craftbox():
    """Shows the signup page"""
    return render_template("craftbox.html")        
    
@app.route('/login')
def show_login():
    """Shows the signup page"""
    return render_template("login.html")    

@app.route('/login', methods=['POST', 'GET'])
def login():
    """Login page for the user"""
    
    if current_user.is_authenticated:
        return redirect('/craftbox')
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = crud.find_user_by_email(email)
        if user is not None and crud.check_password(user, password):
            login_user(user)
            flash(f'Logged in as {user.user_name}.')
            return redirect('/craftbox')
 
    flash('Invalid email or password. Try again.')
    return redirect('/login')


@app.route('/account')
@login_required
def show_account_page():
    """Shows user's account page"""
    pass

@app.route('/logout')
def logout():
    """Logs out for the user""" 
    logout_user()
    return redirect('/')

@app.route('/search')
def user_search():
    """Shows user search results based on their query"""
    pass

@app.route('/selection')
def show_selected_item():
    """Shows page for the selected item"""
    pass

@app.route('/addlink')
@login_required
def show_addlink():
    """Shows the addlink form"""
    return render_template("addlink.html")

@app.route('/addlink', methods=['POST'])
@login_required
def add_link():
    """Allows a user to add a link"""

    name = request.form.get('name')
    link_path = request.form.get('link_path')
    user_id = current_user.user_id
    image = request.form.get('image')
    notes = request.form.get('notes')

    crud.add_link(name, link_path, user_id, image=None, notes=None)
    flash('Link Added!')
    return redirect('/craftbox')

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)