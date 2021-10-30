"""Models for my craft box app."""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import LoginManager



login_manager = LoginManager()
db = SQLAlchemy()



class User(UserMixin, db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    fname = db.Column(db.String (25), nullable=False)
    lname = db.Column(db.String (25), nullable=False)
    user_name = db.Column(db.String (25), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False )
    password_hash = db.Column(db.String(128), nullable=False)


    # links = A list of Link objects
    # tags = A list of Tag objects

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return f'<User user_id={self.user_id} user_name={self.user_name}>'

@login_manager.user_loader
def load_user(user_id):
    """Returns the user_id of the user as an integer."""
    return User.query.get(int(user_id))

class Link(db.Model):
    """A link."""

    __tablename__ = "links"

    link_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    name = db.Column(db.String, nullable=False)
    link_path = db.Column(db.Text, nullable=False)
    image = db.Column(db.String, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    user = db.relationship("User", backref="links")

    # tags = A list of Tags objects w/ secondary backref to TagsLinks

    def __repr__(self):
        return f'<Link link_id={self.link_id} name={self.name}>'

    def conv_to_dict(self):
        """Converts to a dictionary for json"""
        return {
            "link_id": self.link_id,
            "name": self.name, 
            "link_path":self.link_path,
            "image": self.image,
            "notes": self.notes
            }


class Tag(db.Model):
    """A sort tag."""

    __tablename__ = "tags"

    tag_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    tag = db.Column(db.String(25))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    user = db.relationship("User", backref="tags")

    links = db.relationship("Link", secondary="tagslinks", backref="tags")


    def __repr__(self):
        return f'<Tag tag_id={self.tag_id} tag={self.tag}>'
    
    def conv_tag_to_dict(self):
        """Converts to a dictionary for json"""
        return {
            "tag_id": self.tag_id,
            "tag": self.tag
            }

class TagLink(db.Model):
    """Association table for Tag and Link."""

    __tablename__ = "tagslinks"

    tagslinks_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    link_id = db.Column(db.Integer, db.ForeignKey("links.link_id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.tag_id"))

    def __repr__(self):
        return f'<TagLink link_id={self.link_id} tag_id={self.tag_id}>'



def connect_to_db(flask_app, db_uri="postgresql:///craftbox", echo=True):
    """Shortcut function to do connect to the db for the server file to """
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)
    @flask_app.before_first_request
    def create_table():
        db.create_all()

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
