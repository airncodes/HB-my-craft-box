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
    """Shows all the links that a user has added"""
    user = User.query.filter(User.user_id == user_id).first()
    return user.links

def add_note2link():
    """Function to add a note after a link has already been added"""



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


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
