"""Server routes for My Craft Box app."""

from flask import Flask, render_template, request, flash, redirect, jsonify
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

@app.route('/logout')
def logout():
    """Logs out for the user"""
    logout_user()
    return redirect('/')

@app.route('/search', methods=['POST'])
@login_required
def user_search():
    """Shows user search results based on their query NO REACT"""

    query_word = request.form.get('query')
    query_tag = crud.search_by_tag(query_word)
    return render_template("results.html", query_word=query_word, query_tag=query_tag )

@app.route('/addlink')
@login_required
def show_addlink():
    """Shows the addlink form"""
    user_id = current_user.user_id
    tags = crud.show_tags(user_id)
    return render_template("addlink.html", tags=tags)

@app.route('/addlink', methods=['POST'])
@login_required
def add_link():
    """Allows a user to add a link"""

    name = request.form.get('name')
    link_path = request.form.get('link_path')
    user_id = current_user.user_id
    image = request.form.get('image')
    notes = request.form.get('notes')

    # Creates link
    crud.add_link(name, link_path, user_id, image, notes)
    link_req = name
    # If link is tagged, creates the taglink association.
    tags_sel = request.form.getlist("tag2apply")
    if tags_sel:
        crud.apply_tag2link(link_req, tags_sel)
    flash('Link Added!')
    return redirect('/craftbox')

@app.route('/craftbox')
@login_required
def show_craftbox():
    """Shows main craftbox page for React"""
    user_id = current_user.user_id
    links = crud.show_links_of_user(user_id)
    tags = crud.show_tags(user_id)
    return render_template("craftbox.html", tags=tags, links=links)

@app.route('/editcard')
@login_required
def show_edit_card():
    """Shows the addtag form"""
    user_id = current_user.user_id
    links = crud.show_links_of_user(user_id)
    tags = crud.show_tags(user_id)
    return render_template("editcard.html", links=links, tags=tags)

@app.route("/editcard", methods=["POST"])
def edit_card():
    """Add a new card to the DB."""
    name = request.form.get("name")
    image = request.form.get("image")
    notes = request.form.get("notes")
    link_id = request.form.get("link_id")
    print(link_id)
    
    # Iterate through the responses, if responses are not empty call edit function(s) to update the link.
    if name:
        print(name)
        crud.edit_link_name(link_id, name)
    if image:
        crud.edit_link_image(link_id, image)
    if notes:
        print(notes)
        crud.edit_link_notes(link_id, notes)
    else:
        flash('No changes made')
        return redirect('/craftbox')
   
    flash('Link Edited!')

@app.route("/deletecard", methods=["POST"])
def delete_card():
    """Delete a card to the DB."""
    link_id = request.form.get("link_id")
    print(link_id)
    crud.del_link_card(link_id)
   
    flash('Link Removed!')


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

@app.route('/applytaglink', methods=['POST'])
@login_required
def add_tag2link():
    """Allows a user to apply a tag"""
    
    link_req = request.form.get("link")
    tags_sel = request.form.getlist("tag2apply")

    crud.apply_tag2link(link_req, tags_sel)
    flash('Link Tagged!')
    return redirect('/craftbox')



if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
