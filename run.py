from math import ceil
import os
import time
from dhis2 import Api,  pretty_json, setup_logger, logger, load_json
from dhis2.utils import partition_payload
import csv

api = Api.from_auth_file('auth.json')
setup_logger('integration.log')


def import_data(payload, dry_run=True, batch_size=25000):
    # async data import

    if not dry_run:
        logger.warning("Pushing data...")
        time.sleep(3)

    total_values = len(payload["dataValues"])

    if(batch_size == 0):
        batch_size = total_values

    total_pages = ceil(total_values/batch_size)

    for index, data in enumerate(partition_payload(payload, 'dataValues', batch_size), 1):
        job_uid = api.post(
            'dataValueSets', data=data,
            params={'skipAudit': 'true',
                    'async': 'true',
                    'dryRun': str(dry_run).lower(),
                    'skipExistingCheck': 'false',
                    'orgUnitIdScheme': 'code',
                    'importStrategy': 'CREATE_AND_UPDATE',
                    # 'dataElementIdScheme': 'code',
                    'categoryOptionComboIdScheme': 'code'}
        ).json()['response']['id']
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


def load_csv(path):
    with open(path, newline='\n', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def main():
    # data = load_json(os.path.join('dummydata', 'newFamilies.json'))
    raw_data = load_csv(os.path.join('dummydata', 'premium_collected.csv'))
    data = {"dataValues": raw_data}
    import_data(data, dry_run=False, batch_size=25000)
    # pretty_json(data["dataValues"][0])


if __name__ == '__main__':
    main()
