import argparse
import datetime
import sys

from dhis2 import setup_logger, logger
from engine.dhis import import_data
from engine.model import Integration
from integrations import (
    newfamilies,
    newinsurees,
    newpolicies,
    premiumcollection,
    renewals,
    numberofclaims,
    claimsvaluated
)
from engine.db import execute_query
from version import app_name

setup_logger('integration.log')


def process_families(date_from, date_to, dry_run):
    integration = Integration(newfamilies.query.format(
        date_from=date_from, date_to=date_to), newfamilies.parameters, "New Families")

    payload = execute_query(integration.query)
    import_data(payload, integration.parameters, dry_run)


def process_insurees(date_from, date_to, dry_run):
    integration = Integration(newinsurees.query.format(
        date_from=date_from, date_to=date_to), newinsurees.parameters, "New Insurees")
    payload = execute_query(integration.query)
    import_data(payload, integration.parameters, dry_run)


def process_new_policies(date_from, date_to, dry_run):
    integration = Integration(newpolicies.query.format(
        date_from=date_from, date_to=date_to), newpolicies.parameters, dry_run)
    payload = execute_query(integration.query)
    import_data(payload, integration.parameters, dry_run)


def process_premium_collection(date_from, date_to, dry_run):
    integration = Integration(premiumcollection.query.format(
        date_from=date_from, date_to=date_to), premiumcollection.parameters, "Premium Collection")
    payload = execute_query(integration.query)
    import_data(payload, integration.parameters, dry_run)


def process_renewals(date_from, date_to, dry_run):
    integration = Integration(renewals.query.format(
        date_from=date_from, date_to=date_to), renewals.parameters, "Renewals")
    payload = execute_query(integration.query)
    import_data(payload, integration.parameters, dry_run)


def process_numberofclaims(date_from, date_to, dry_run):
    integration = Integration(numberofclaims.query.format(
        date_from=date_from, date_to=date_to), numberofclaims.parameters, "Number of Claims")
    payload = execute_query(integration.query)
    import_data(payload, integration.parameters, dry_run)


def process_claimsvaluated(date_from, date_to, dry_run):
    integration = Integration(claimsvaluated.query.format(
        date_from=date_from, date_to=date_to), claimsvaluated.parameters, "Claims Valuated")
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
    parser.add_argument("-v", "--version",
                        help="Gives the current version",
                        action="version",
                        version=app_name
                        )

    return parser.parse_args()


def main(args):
    logger.info(app_name)
    process_families(args.date_from, args.date_to, args.dry_run)
    process_insurees(args.date_from, args.date_to, args.dry_run)
    process_new_policies(args.date_from, args.date_to, args.dry_run)
    process_premium_collection(args.date_from, args.date_to, args.dry_run)
    process_renewals(args.date_from, args.date_to, args.dry_run)
    process_numberofclaims(args.date_from, args.date_to, args.dry_run)
    process_claimsvaluated(args.date_from, args.date_to, args.dry_run)


if __name__ == '__main__':
    args = parse_args()

    main(args)
