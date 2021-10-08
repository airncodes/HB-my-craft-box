from flask import (Flask, render_template, request, flash, session, redirect)
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
def sign_up():
    """User sign up"""
    pass

@app.route('/login')
def login_user():
    """Login page for the user"""
    pass

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

@app.route('/add')
def add_item():
    """Allows a user to add a link and/or tag"""
    pass

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)