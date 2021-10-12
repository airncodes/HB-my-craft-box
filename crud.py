"""CRUD Operations for Model"""

from model import db, User, Link, Tag, TagLink, connect_to_db
from werkzeug.security import generate_password_hash, check_password_hash


# User/Account Functions
def create_user(fname, lname, user_name, email, password_hash):
    # Adds user to database
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
    #Finds a user by their email.

    return User.query.filter(User.email == email).first()

def get_userid_by_email(email):
    # Gets the user id of the user by their email used to login.
    user_info = find_user_by_email(email)
    return user_info.user_id

def set_password(user, password):
        user.password_hash = generate_password_hash(password)


def check_password(user, password):
    return check_password_hash(user.password_hash, password)

# Link Functions
def add_link(name, link_path, user_id, image=None, notes=None):
    # Adds link to database.
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

def add_note2link():
    pass

# Tag Functions
def add_tag(tag):
    # Adds tag to database
    tag = Tag(
        tag=tag,
    )

    db.session.add(tag)
    db.session.commit()

    return tag

def apply_tag2link():
    pass

def search_by_tag():
    pass

# TagLink Functions
def create_taglink(link_id, tag_id):
    # Adds taglink to the database to connect tags with links. 
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