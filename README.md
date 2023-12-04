# electronics_platform

### This API could be used for organization of Online electronics retail platform.

##### The following features are implemented:
* Authorization and authentication of users(Djoser is used);
* CRUD for different parts of retail network with automatic assignment of hierarchy level;
* Django admin panel, with links for Supplier, filter by city, admin action for debt nullification for several nodes at once;
* Permissions: only authorized users are allowed to use API, debs could not be updated by API directly;
* Filter by country inside the NetworkNode model.
* Documentation (both Swagger and Redoc are available)

## Start project

### .env

It is necessary to create .env file for this project. You can file the structure for the file in .env.example

### Running the project

To run the project install all dependencies:\
`pip install -r requirements.txt`

Create database:\
`psql -U username` (change to your username in postgres)\
`CREATE DATABASE *databasename*;` (change to your database name that you've included in your .env)


Apply migrations:\
`python manage.py migrate`

Run server:\
`python manage.py runserver`

To run tests use:\
`coverage run --source='.' manage.py test`
