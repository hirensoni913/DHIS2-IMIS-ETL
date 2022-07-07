## Install

Requirements: Python 3

* Copy file `auth.json.example` to `auth.json`
* Update credentials in `auth.json`
* Install dependencies:

```
python3 -m virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```
# if you have not done so already above:
source .venv/bin/activate

python download.py
```

will download metadata in the `metadata` folder.


## Import metadata

* Use the DHIS2 app `Import/Export` and navigate to _Metadata import_.
