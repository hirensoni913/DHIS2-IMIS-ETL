import argparse
import datetime
import sys

from dhis2 import setup_logger, logger
from pyodbc import lowercase
from engine.dhis import import_data, fetch_metadata
from engine.model import Integration
from integrations import (
    newfamilies,
    newinsurees,
    newpolicies,
    premiumcollection,
    renewals,
    numberofclaims,
    claimsvaluated,
    healthfacilities,
    metadata
)
from engine.db import execute_query
from version import app_name

setup_logger('integration.log')


def process_families(date_from, date_to, dry_run):
    print("")
    logger.info("Importing Families")
    integration = Integration(newfamilies.query.format(
        date_from=date_from, date_to=date_to), newfamilies.parameters, "New Families")

    payload = execute_query(integration.query)
    import_data(payload, integration.parameters, dry_run)


def process_insurees(date_from, date_to, dry_run):
    print("")
    logger.info("Importing Insurees")
    integration = Integration(newinsurees.query.format(
        date_from=date_from, date_to=date_to), newinsurees.parameters, "New Insurees")
    payload = execute_query(integration.query)
    import_data(payload, integration.parameters, dry_run)


def process_new_policies(date_from, date_to, dry_run):
    print("")
    logger.info("Importing Policies")
    integration = Integration(newpolicies.query.format(
        date_from=date_from, date_to=date_to), newpolicies.parameters, dry_run)
    payload = execute_query(integration.query)
    import_data(payload, integration.parameters, dry_run)


def process_premium_collection(date_from, date_to, dry_run):
    print("")
    logger.info("Importing Premium")
    integration = Integration(premiumcollection.query.format(
        date_from=date_from, date_to=date_to), premiumcollection.parameters, "Premium Collection")
    payload = execute_query(integration.query)
    import_data(payload, integration.parameters, dry_run)


def process_renewals(date_from, date_to, dry_run):
    print("")
    logger.info("Importing Renewals")
    integration = Integration(renewals.query.format(
        date_from=date_from, date_to=date_to), renewals.parameters, "Renewals")
    payload = execute_query(integration.query)
    import_data(payload, integration.parameters, dry_run)


def process_numberofclaims(date_from, date_to, dry_run):
    print("")
    logger.info("Importing Claims")
    integration = Integration(numberofclaims.query.format(
        date_from=date_from, date_to=date_to), numberofclaims.parameters, "Number of Claims")
    payload = execute_query(integration.query)
    import_data(payload, integration.parameters, dry_run)


def process_claimsvaluated(date_from, date_to, dry_run):
    print("")
    logger.info("Importing Valuated Claims")
    integration = Integration(claimsvaluated.query.format(
        date_from=date_from, date_to=date_to), claimsvaluated.parameters, "Claims Valuated")
    payload = execute_query(integration.query)
    import_data(payload, integration.parameters, dry_run)


def process_healthfacilities(dry_run):
    print("")
    logger.info("Importing Health Facilities")
    existing_ous = fetch_metadata("organisationUnits")
    existing_ous = list(existing_ous.items())
    integration = Integration(healthfacilities.query,
                              None, "Health Facilities")
    hfs = execute_query(integration.query)

    print(hfs)
    metadata.prepare_hf_payload(
        hfs, existing_ous, metadata.Strategy.INSERT)


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
    parser.add_argument("-e", "--entity",
                        help="Specify (comma separated) what data needs to be imported (* = all, families, insurees, newpolicies, premiums, renewals, claims, valuatedclaims)",
                        required=True,
                        type=str
                        )
    parser.add_argument("-v", "--version",
                        help="Gives the current version",
                        action="version",
                        version=app_name
                        )

    return parser.parse_args()


def main(args):
    logger.info(app_name)
    entities = str.split(args.entity, ",")

    if "families" in (entity.lower() for entity in entities) or "*" in entities:
        process_families(args.date_from, args.date_to, args.dry_run)
    if "insurees" in (entity.lower() for entity in entities) or "*" in entities:
        process_insurees(args.date_from, args.date_to, args.dry_run)
    if "newpolicies" in (entity.lower() for entity in entities) or "*" in entities:
        process_new_policies(args.date_from, args.date_to, args.dry_run)
    if "premiums" in (entity.lower() for entity in entities) or "*" in entities:
        process_premium_collection(args.date_from, args.date_to, args.dry_run)
    if "renewals" in (entity.lower() for entity in entities) or "*" in entities:
        process_renewals(args.date_from, args.date_to, args.dry_run)
    if "claims" in (entity.lower() for entity in entities) or "*" in entities:
        process_numberofclaims(args.date_from, args.date_to, args.dry_run)
    if "valuatedclaims" in (entity.lower() for entity in entities) or "*" in entities:
        process_claimsvaluated(args.date_from, args.date_to, args.dry_run)
    if "healthfacilities" in (entity.lower() for entity in entities) or "*" in entities:
        process_healthfacilities(args.dry_run)


if __name__ == '__main__':
    args = parse_args()

    main(args)
