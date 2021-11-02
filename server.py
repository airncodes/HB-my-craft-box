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

@app.route('/results')
@login_required
def user_search():
    """Shows user search results based on their query"""

    # query_word = request.get_json().get('query')
    # fcards = crud.search_by_tag(query_word)
    return render_template("results.html")

@app.route('/craftboxr.json', methods=['POST', 'GET'])
@login_required
def show_results_cards():
    """Shows links of the user""" 
    print('**********')
    print("I am about to print...")
    print(request.form.to_dict(flat=False))
    query_wd = request.get_json().get("tag")
    print('**********')
    print("Next printing query_word")
    print(query_wd)
    fcards = crud.search_by_tag(query_wd) # Filtered Cards
    print('**********')
    print(fcards)
    return jsonify({"fcards": fcards})


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
    """Shows main craftbox page"""
    return render_template("craftboxR.html")

@app.route('/craftboxb.json')
@login_required
def show_tags():
    """Shows tags of the user"""
    user_id = current_user.user_id
    buttons = crud.conv_tags_for_react(user_id)
    return jsonify({"buttons": buttons})

@app.route('/craftbox.json')
@login_required
def show_links_cards():
    """Shows links of the user"""
    user_id = current_user.user_id
    cards = crud.show_links_of_user(user_id)

    # Cards is [<Link >, <Link >]
    # Convert this:[<Link >, <Link >]
    # To:[{"name": }, {}]
    return jsonify({"cards": cards})

@app.route("/edit-card", methods=["POST"])
def edit_card():
    """Add a new card to the DB."""
    name = request.get_json().get("name")
    image = request.get_json().get("image")
    notes = request.get_json().get("notes")
    link_id = request.get_json().get("link_id")
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
   
    
    flash('Link Edited!')
    return jsonify()

@app.route("/del-card", methods=["POST"])
def delete_card():
    """Delete a card to the DB."""
    link_id = request.get_json().get("link_id")
    print(link_id)
    crud.del_link_card(link_id)
   
    flash('Link Removed!')
    return jsonify()


# @app.route('/craftboxF.json', methods=['POST'])
# @login_required
# def filter_view():
#     """Shows user a filterable view of their link cards"""
#     user_id = current_user.user_id
    
#     cards = crud.show_links_of_user(user_id) # All Cards
#     query_word = request.form.get('tag').title() 
#     fcards = crud.filter_by_tag(query_word) # Filtered Cards
#     return jsonify({"fcards": fcards, "cards": cards})


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
