## Install

Requirements: Python 3

Create .env file

```
SERVER=
DATABASE=
DBUSERNAME=
DBPASSWORD=
DHIS2USERNAME=
DHIS2PASSWORD=
DHIS2BASEURL=
```

Install dependencies:

```
python3 -m virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```
# Activate the virtual environment if it's not activated yet:

python run.py --help
```
