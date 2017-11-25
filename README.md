hug-sqlalchemy-template
=======================

Hug project skeleton with working sqlalchemy connections tests and migrations framework already set up.
Basically it's good entry point to develop every kind of sqlalchemy powered api using hug.

## Prerequisites
It runs only with Python 3

## Installation
```
git clone https://github.com/FutureMind/hug-sqlalchemy-template.git
pip install -r requirements.txt
gunicorn --reload api.app:__hug_wsgi__
```
API will be exposed locally to http://127.0.0.1:8000

## Database
Provide SQLALCHEMY_DATABASE_URI and TEST_SQLALCHEMY_DATABASE_URI environment variables.
If TEST_SQLALCHEMY_DATABASE_URI is not provided it will be automatically set to SQLALCHEMY_DATABASE_URI + '_test' suffix

## Migrations
Project uses alembic to manage migrations script
http://alembic.zzzcomputing.com/en/latest/

### Example usage 
Add new migrations with
```
alembic revision --autogenerate -m "migration name"
```
Upgrade your database with
```
alembic upgrade head
```

## Tests
Put your tests into tests module.
Run your tests with
```
python -m pytest
```

## Examples
You can see some basic examples of how set up models, authentication and routes on `user_jwt_auth_example_project` branch

There is also an example how to implement application factory (just like we do in flask http://flask.pocoo.org/docs/0.12/patterns/appfactories/) on `app_constructor_example`
