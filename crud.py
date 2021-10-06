"""CRUD Operations for Model"""

from model import db, User, Movie, Rating, connect_to_db
# User/Account Functions
def create_user():
    pass


# Link Functions
def add_link():
    pass

def add_note2link():
    pass

# Tag Functions
def add_tag():
    pass

def apply_tag2link():
    pass

def search_by_tag():
    pass

if __name__ == '__main__':
    from server import app
    connect_to_db(app)