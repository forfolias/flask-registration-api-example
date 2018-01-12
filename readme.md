# Basic User Registration REST Example Using Flask

## Requirements
Make sure you have installed 
* Python 3.6
* python-venv
* python-pip

## Local Setup Instructions

### 1. Initialize and activate virtualenv for the project
```
$ python3.6 -m venv venv
$ . venv/bin/activate
```

### 2. Install required dependencies
```
(venv) pip install -r requirements.txt
```

### 3. Configure project
Create `instance/config.py` and set the `SQLALCHEMY_DATABASE_URI` option.

### 4. Apply pending database migrations
```
(venv) FLASK_APP=run.py flask db upgrade
```

### 5. Run the application
```
(venv) FLASK_APP=run.py flask run
```

### 6. Make a test request
```
$ curl -X POST http://127.0.0.1:5000/register -F name='Full Name' -F email=email@address.com
```

## Running Unit tests
```
(venv) python3.6 test.py
```
