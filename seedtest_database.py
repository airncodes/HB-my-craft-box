"""Script to seed test database."""

# All the imports
import os
import json
from random import choice

import crud
import model
import server

os.system("dropdb craftbox")
os.system("createdb craftbox")

model.connect_to_db(server.app)
model.db.create_all()

# Create 10 users
db_users = []
for n in range(10):
    fname = f"Test{n}"
    lname = f"McTester{n}"
    user_name = f"test_user{n}"
    email = f"user{n}@test.com"  
    password = "test"

    db_user = crud.create_user(fname, lname, user_name, email, password)
    db_users.append(db_user)

# Create links
# 1. Load link data from JSON file
with open("data/testlinks.json") as l:
    link_data = json.loads(l.read())
# 2. Iterate through all the links in the link data to create each "link". 

for link in link_data:
    name, link_path, image, notes = (
        link["name"],
        link["link_path"],
        link.get("image"),
        link.get("notes")
    )
    rand_user = choice(db_users)
    user_id = rand_user.user_id
    
    db_link = crud.add_link(name, link_path, user_id, image=image, notes=image)


# Create 10 tags
for n in range(10):
    tag = f"Test_tag{n}"

    db_tag = crud.add_tag(tag)

