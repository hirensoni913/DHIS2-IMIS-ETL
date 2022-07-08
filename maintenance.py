import json
import os
import time
from dhis2 import Api,  pretty_json, setup_logger, logger, load_json
from dhis2.utils import partition_payload
import csv
from dotenv import load_dotenv

load_dotenv()

api = Api(server=os.getenv("DHIS2BASEURL"), username=os.getenv("DHIS2USERNAME"),
          password=os.getenv("DHIS2PASSWORD"))


def delete_dataelements_list():
    uids = ['IiTYUcWbGzO',
            'iOMBWxL1eOn',
            'D3QO0idBBWA',
            'Nqs5TA2YwbM',
            'pMe4Z8R9I7y']

    for uid in uids:
        resp = api.delete(f'dataElements/{uid}')
        print(resp.text)


def update_org_unit():
    data = api.get_paged('organisationUnits', params={
                         'fields': ':owner'}, page_size=1000, merge=True)["organisationUnits"]
    payload = {"organisationUnits": []}
    for ou in data:
        if " - " in ou["name"]:
            code, name = ou["name"].split(" - ", 1)
            ou["name"] = f'{name} ({code})'

        payload["organisationUnits"].append(ou)

    with open("orgUnits.json", "w") as f:
        json.dump(payload, f, indent=2)


update_org_unit()
