# Tagfolio Simple API

## How to run this backend server

### Step 0: Clone and install the dependencies

This project is managed by pipenv

- Install pipenv
  > pip install pipenv
- Install Dependencies
  > pipenv install

### Step 1: Run the database

Go to the tagfoliops repository and run the docker-compose file in database folder

### Step 2: Add dummy data in the database

In the root of this application there is a migrations.py file. Run it as

python migrations.py

### Step 3: Run the server

> pipenv shell
> python api.py
