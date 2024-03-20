# Tagfolio Simple API

## How to run this backend server

### Step 0: Clone and install the dependencies

python -m venv environ
pip install -r requirements.txt

### Step 1: Run the database

Go to the tagfoliops repository and run the docker-compose file in database folder

### Step 2: Add dummy data in the database

In the root of this application there is a migrations.py file. Run it as

python migrations.py

### Step 3: Run the server

python api.py
