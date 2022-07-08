import time
from math import ceil
import os

from dhis2 import Api,  logger
from dhis2.utils import partition_payload
from dotenv import load_dotenv

from version import app_name

load_dotenv()

api = Api(server=os.getenv("DHIS2BASEURL"), username=os.getenv("DHIS2USERNAME"),
          password=os.getenv("DHIS2PASSWORD"), user_agent=app_name)


def import_data(payload: list, parameters: dict, dry_run=True, batch_size=25000):
    # async data import
    payload = {"dataValues": payload}
    if not dry_run:
        logger.warning("Pushing data...")
        time.sleep(3)

    total_values = len(payload["dataValues"])

    if(batch_size == 0):
        batch_size = total_values

    total_pages = ceil(total_values/batch_size)
    def_parameters = {'skipAudit': 'true',
                      'async': 'true',
                      'dryRun': str(dry_run).lower()
                      }
    params = def_parameters | parameters

    for index, data in enumerate(partition_payload(payload, 'dataValues', batch_size), 1):
        job_uid = api.post(
            'dataValueSets', data=data,
            params=params).json()['response']['id']
        logger.info(
            f"{index} / {total_pages} Data import job started: {job_uid} - waiting...")
        while True:
            ping = api.get(f'system/tasks/DATAVALUE_IMPORT/{job_uid}')
            ping.raise_for_status()
            done = [item for item in ping.json() if item['completed']
                    is True and item['message'] == 'Import done']
            if done:
                summary = api.get(
                    f'system/taskSummaries/DATAVALUE_IMPORT/{job_uid}').json()
                logger.info(
                    f"{summary.get('description')} - {summary.get('importCount')}")
                break

            error = [item for item in ping.json() if item['level'] == 'ERROR']
            if error:
                logger.error(ping.json())
                break
            time.sleep(0.5)
