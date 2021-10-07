"""CRUD Operations for Model"""

from model import db, User, Link, Tag, TagLink, connect_to_db
# User/Account Functions
def create_user(fname, lname, user_name, email, password):
    user = User(
        fname=fname, 
        lname=lname, 
        user_name=user_name, 
        email=email, 
        password=password
        )

    db.session.add(user)
    db.session.commit()

    return user

# Link Functions
def add_link(name, link_path, user_id, image=None, notes=None):
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
    taglink = TagLink(
        link_id=link.link_id, 
        tag_id=tag.tag_id
        )
    
    db.session.add(taglink)
    db.session.commit()

    return taglink


if __name__ == '__main__':
    from server import app
    connect_to_db(app)