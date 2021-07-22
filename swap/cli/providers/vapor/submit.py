#!/usr/bin/env python
# coding=utf-8

import sys

from ....cli import click
from ....providers.vapor.utils import submit_transaction_raw


@click.command("submit", options_metavar="[OPTIONS]",
               short_help="Select Vapor Transaction raw submitter.")
@click.option("-tr", "--transaction-raw", type=str, required=True, help="Set signed Vapor transaction raw.")
def submit(transaction_raw: str):
    try:
        click.echo(
            submit_transaction_raw(
                transaction_raw=transaction_raw
            )["transaction_hash"]
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
