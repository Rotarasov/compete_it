# Compete IT
Compete IT is a project aimed to help students to find the most relevant competitions in IT and teammates for a team contests! <br>
This repo contains only API of the project<br>
**Technologies:** Django, Django REST Framework, Django Channels<br>
**Databases:** PostgreSQL(Production), SQLite(Development), Redis<br>
**Deployment:** Heroku, Cloudinary
## Prerequisites
- Python installed version 3.8.5
- `virtualenv` installed globally via pip
## Installation
1. Clone git repo using command `git clone https://github.com/Rotarasov/Compete-IT.git`
2. Go to folder `cd compete_it` and create virtual environment `virtaulenv venv`
3. Install requirements from txt file `pip install -r requirements.txt`
4. Add database url and variable for local development to .env file `echo -e "DATABASE_URL=sqlite:///db.sqlite3\nLOCAL=1" > .env`
5. Create database `touch db.sqlite`
6. Create folders for media `mkdir -p media/{user_pics,event_pics}` and upload to media/user_pics picture for default user image and the name should be `default.png`
7. Run `python manage.py migrate` in the command line to set up database
8. Run `python manage.py runserver` to run server
