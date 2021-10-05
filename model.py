"""Models for my craft box app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    fname = db.Colimn(db.String (25), nullable=False)
    lname = db.Colimn(db.String (25), nullable=False)
    user_name = db.Colimn(db.String (25), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False )
    password = db.Column(db.String(50), nullable=False)

    # links = A list of Link objects

    def __repr__(self):
        return f'<User user_id={self.user_id} user_name={self.user_name}>'


class Link(db.Model):
    """A link."""

    __tablename__ = "links"

    link_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    name = db.Column(db.String, nullable=False)
    link_path = db.Column(db.Text, nullable=False)
    image = db.Column(db.String, nullable=True)
    notes = db.Column(db.Text, nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    user = db.relationship("User", backref="links")

    # tagslinks = A list of TagLink objects

    def __repr__(self):
        return f'<Link link_id={self.link_id} name={self.name}>'

class Tag(db.Model):
    """A sort tag."""

    __tablename__ = "tags"

    tag_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    tag = db.Column(db.String(25))
    
    # tagslinks = A list of TagLink objects

    def __repr__(self):
        return f'<Tag tag_id={self.tag_id} tag={self.tag}>'

class TagLink(db.Model):
    """Association table for Tag and Link."""

    __tablename__ = "tagslinks"

    tagslinks_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    link_id = db.Column(db.Integer, db.ForeignKey("links.link_id")) 
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.tag_id"))

    link = db.relationship("Link", backref="tagslinks")
    tag = db.relationship("Tag", backref="tagslinks")

    def __repr__(self):
        return f'<Rating rating_id={self.rating_id} score={self.score}>'



def connect_to_db(flask_app, db_uri="postgresql:///craftbox", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
