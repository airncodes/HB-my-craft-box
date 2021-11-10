# MyCraftBox
Have you ever struggled to remember where you saved a certain recipe or which YouTube video helped you on learning a new skill? MyCraftBox is here to help! MyCraftBox is an all-in-one app that allows you to store all your favorite links, tag them however you like, and add notes to them in the form of cards. If the links are tagged, then you can go back and search by tag and that will render all the links associated with the tag. 

# Table of Contents
- [Technologies, Tools, and Libraries Used](https://github.com/airncodes/HB-my-craft-box/new/main?readme=1#technologies-tools-and-libraries-used)
- [Running your own MyCraftBox locally](https://github.com/airncodes/HB-my-craft-box/new/main?readme=1#running-your-own-mycraftbox-locally)
- [Using MyCraftBox](https://github.com/airncodes/HB-my-craft-box/new/main?readme=1#running-your-own-mycraftbox-locally)

# Technologies, Tools, and Libraries Used
- Python
- Flask
- PostgreSQL
- SQLAlchemy
- Werkzeug
- Flask-Login
- JavaScript
- React
- JSON
- Jinja
- Boostrap
- CSS
- HTML

# Running your own MyCraftBox locally
MyCraftBox is not deployed so the app would need to be ran locally to use. 
- Set up and activate your virtualenv, and install all dependencies from the requirements.txt file:
`pip3 install -r requirements.txt`
- Create a new database named craftbox:
`$ createdb craftbox`
- The tables will be created on initial start up before the first flask request. 
- There is no need to seed any databases but a sample on is provided.
`testlinks.json`
- Run the server in interactive mode:
`python3 -i server.py`
- See the app running by going to localhost:5000
