"""Script to seed test database."""

# All the imports
import os
from random import choice

import crud
import model
import server



# Create 10 users
for n in range(10):
    fname = f"Test{n}"
    lname = f"McTester{n}"
    user_name = f"test_user{n}"
    email = f"user{n}@test.com"  
    password = "test"

    user = crud.create_user(fname, lname, user_name, email, password)

# Create links


# Create tags