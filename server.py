"""Server routes for My Craft Box app."""

from flask import Flask, render_template, request, flash, redirect
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


# @app.route('/account')
# @login_required
# def show_account_page():
#     """Shows user's account page"""
#     if request.method == "POST":
#         fname = request.form.get('fname')
#         lname = request.form.get('lname')
#         user_name = request.form.get('user_name')
#         email = request.form.get('email')
        

#         if email != current_user.email:
#             current_user.email=email
#             db.session.commit()
#             flash('Email updated')
#         user = crud.find_user_by_email(email)
#         if user:
#             flash('Email already taken')
            
#     return render_template("accounts_page.html",)

@app.route('/logout')
def logout():
    """Logs out for the user"""
    logout_user()
    return redirect('/')

@app.route('/search', methods=['POST'])
@login_required
def user_search():
    """Shows user search results based on their query"""

    query_word = request.form.get('query')
    query_tag = crud.search_by_tag(query_word)
    return render_template("results.html", query_word=query_word, query_tag=query_tag)

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

    crud.add_link(name, link_path, user_id, image, notes)
    flash('Link Added!')
    return redirect('/craftbox')

@app.route('/craftbox')
@login_required
def show_tags():
    """Shows links of the user"""
    user_id = current_user.user_id
    tags = crud.show_tags(user_id)
    return render_template("craftbox.html", tags=tags)

@app.route('/craftbox.json')
@login_required
def show_links_cards():
    """Shows links of the user"""
    user_id = current_user.user_id
    links = crud.show_links_of_user(user_id)
    return jsonify(links)

@app.route('/addtag')
@login_required
def show_addtag():
    """Shows the addtag form"""
    return render_template("addtag.html")

@app.route('/addtag', methods=['POST'])
@login_required
def add_tag():
    """Allows a user to add a link"""

    tag = request.form.get('tag')
    user_id = current_user.user_id

    crud.add_tag(tag, user_id)
    flash('Tag Added!')
    return redirect('/craftbox')

@app.route('/applytaglink')
@login_required
def applytaglink():
    """Apply tag(s) to a link form"""
    user_id = current_user.user_id
    links = crud.show_links_of_user(user_id)
    tags = crud.show_tags(user_id)
    return render_template("applytaglink.html", links=links, tags=tags)

@app.route('/applytaglink', methods=['POST', 'GET'])
@login_required
def add_tag2link():
    """Allows a user to apply a tag"""
    if request.method == 'POST':
        link_req = request.form.get("link")
        # print(link_req)
        tags_sel = request.form.getlist("tag2apply")
        # print(tags_sel)

        crud.apply_tag2link(link_req, tags_sel)
        flash('Link Tagged!')
        return redirect('/craftbox')



if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
