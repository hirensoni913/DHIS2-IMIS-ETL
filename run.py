import argparse
from ast import Store
import datetime
from math import ceil
import os
import sys
import time
from xmlrpc.client import boolean
from dhis2 import Api,  pretty_json, setup_logger, logger, load_json
from dhis2.utils import partition_payload
import csv
from engine.model import Integration
from integrations import (
    newfamilies,
    premiumcollection
)
from engine.db import execute_query

api = Api.from_auth_file('auth.json')
setup_logger('integration.log')


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


def load_csv(path):
    with open(path, newline='\n', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def process_families(date_from, date_to, dry_run):
    integration = Integration(newfamilies.query.format(
        date_from=date_from, date_to=date_to), newfamilies.parameters, "New Families")

    payload = execute_query(integration.query)
    import_data(payload, integration.parameters, dry_run)


def process_premium_collection(date_from, date_to, dry_run):
    integration = Integration(premiumcollection.query.format(
        date_from=date_from, date_to=date_to), premiumcollection.parameters, "Premium Collection")
    payload = execute_query(integration.query)
    import_data(payload, integration.parameters, dry_run)


def parse_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--date_from",
                        help="The From Date - format YYYY-MM-DD",
                        required=True,
                        type=datetime.date.fromisoformat)
    parser.add_argument("-t", "--date_to",
                        help="The To Date - format YYYY-MM-DD",
                        required=True,
                        type=datetime.date.fromisoformat)
    parser.add_argument("-d", "--dry_run",
                        help="Specify if this is a dry run",
                        action="store_true",
                        )

    return parser.parse_args()


def main(args):
    process_families(args.date_from, args.date_to, args.dry_run)
    process_premium_collection(args.date_from, args.date_to, args.dry_run)


if __name__ == '__main__':
    args = parse_args()

    main(args)
