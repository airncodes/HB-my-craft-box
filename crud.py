"""CRUD Operations for Model"""

from model import db, User, Link, Tag, TagLink, connect_to_db
from werkzeug.security import generate_password_hash, check_password_hash



# User/Account Functions
def create_user(fname, lname, user_name, email, password_hash):
    """Adds user to database"""
    user = User(
        fname=fname,
        lname=lname,
        user_name=user_name,
        email=email,
        password_hash=password_hash
        )

    db.session.add(user)
    db.session.commit()

    return user

def find_user_by_email(email):
    """ Finds a user by their email. """

    return User.query.filter(User.email == email).first()

def get_userid_by_email(email):
    """Gets the user id of the user by their email used to login."""
    user_info = find_user_by_email(email)
    return user_info.user_id

def set_password(user, password):
    """Sets the password hash"""
    password_hash = generate_password_hash(password)
    return password_hash

def check_password(user, password):
    """Checks that the input password matches the stored password"""
    return check_password_hash(user.password_hash, password)



# Link Functions
def add_link(name, link_path, user_id, image=None, notes=None):
    """Adds link to database."""
    link = Link(
        name=name,
        link_path=link_path,
        image=image,
        notes=notes,
        user_id=user_id,
    )

    db.session.add(link)
    db.session.commit()

    return link


def show_links_of_user(user_id):
    """Shows all the links that a user has added and converts the objects from a list of 
    objects to a list of of dictionaries"""
    user = User.query.filter(User.user_id == user_id).first()
    return user.links


## Edit link card functions.
# def edit_link_name(link_req, name):
#     """Edits the name of a link record"""
#     to_edit = Link.query.filter(Link.name==link_req).first()
#     to_edit.name = name
#     db.session.commit()


# def edit_link_image(link_req, image):
#     """Edits the image path of a link record"""
#     to_edit = Link.query.filter(Link.name==link_req).first()
#     to_edit.image = image
#     db.session.commit()


# def edit_link_notes(link_req, notes):
#     """Function to add or edit a note after a link has already been added"""
    
#     to_edit = Link.query.filter(Link.name==link_req).first()
#     to_edit.notes = notes
#     db.session.commit()


# def del_link_card(link_req):
#     """Function to delete a card."""
#     to_delete = Link.query.filter(Link.name==link_req).first()
#     db.session.delete(to_delete)
#     db.session.commit()

# Tag Functions

def add_tag(tag, user_id):
    """Adds tag to database"""
    tag = Tag(
        tag=tag,
        user_id=user_id,
    )

    db.session.add(tag)
    db.session.commit()

    return tag

def show_tags(user_id):
    """Shows all tags"""
    user = User.query.filter(User.user_id == user_id).first()
    return user.tags

def apply_tag2link(link_req, tags_sel):
    """Function to add a tag to a link."""
    # param1 is passing in link_req and is one item
    # param2 is passing in tags_sel and is a list
    requested_link = Link.query.filter(Link.name==link_req).first()
    for sel_tag in tags_sel:
        use_tag = Tag.query.filter(Tag.tag==sel_tag).first()
        linked_tag = TagLink(link_id=requested_link.link_id, tag_id=use_tag.tag_id)
        db.session.add(linked_tag)
        db.session.commit()

    return linked_tag


def search_by_tag(query_word):
    """Seach by tag"""
    query_tag = Tag.query.filter(Tag.tag.like(f'%{query_word}%')).first()
    return query_tag
    
    
def del_tag(tag_sel):
    """Function to delete a tag."""
    to_delete = Tag.query.filter(Tag.tag==tag_sel).first()
    db.session.delete(to_delete)
    db.session.commit()

# TagLink Functions
def create_taglink(link_id, tag_id):
    """Adds taglink to the database to connect tags with links."""
    taglink = TagLink(
        link_id=link_id,
        tag_id=tag_id
        )

    db.session.add(taglink)
    db.session.commit()

    return taglink

## Card functions for React.
def show_react_links_of_user(user_id):
    """Shows all the links that a user has added and converts the objects from a list of 
    objects to a list of of dictionaries for React"""
    user = User.query.filter(User.user_id == user_id).first()
    return [ link.conv_to_dict() for link in user.links ]



def edit_link_name_react(link_id, name):
    """Edits the name of a link record for React"""
    to_edit = Link.query.get(link_id)
    to_edit.name = name
    db.session.commit()


def edit_link_image_react(link_id, image):
    """Edits the image path of a link record for React"""
    to_edit = Link.query.get(link_id)
    to_edit.image = image
    db.session.commit()


def edit_link_notes_react(link_id, notes):
    """Function to add or edit a note after a link has already been added for React"""
    to_edit = Link.query.get(link_id)
    to_edit.notes = notes
    db.session.commit()


def del_link_card_react(link_id):
    """Function to delete a card for React."""
    to_delete = Link.query.get(link_id)
    db.session.delete(to_delete)
    db.session.commit()

def del_tag_react(link_id):
    """Function to delete a card for React."""
    to_delete = Tag.query.get(link_id)
    db.session.delete(to_delete)
    db.session.commit()

def conv_tags_for_react(user_id):
    """Shows all tags for the user and converts them to a dictionary for React"""
    user = User.query.filter(User.user_id == user_id).first()
    return [ tag.conv_tag_to_dict() for tag in user.tags ]
    


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
