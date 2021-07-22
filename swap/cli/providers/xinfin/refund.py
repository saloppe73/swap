#!/usr/bin/env python
# coding=utf-8

import sys

from ....cli import click
from ....providers.xinfin.transaction import RefundTransaction
from ....providers.config import xinfin as config


@click.command("refund", options_metavar="[OPTIONS]",
               short_help="Select XinFin Refund transaction builder.")
@click.option("-th", "--transaction-hash", type=str, required=True, help="Set XinFin funded transaction hash/id.")
@click.option("-a", "--address", type=str, required=True, help="Set XinFin sender address.")
@click.option("-ca", "--contract-address", type=str, default=None,
              help="Set XinFin HTLC contact address.  [default: None]")
@click.option("-n", "--network", type=str, default=config["network"],
              help="Set XinFin network.", show_default=True)
def refund(transaction_hash: str, address: str, contract_address: str,  network: str):
    try:
        click.echo(
            RefundTransaction(
                network=network
            ).build_transaction(
                address=address,
                transaction_hash=transaction_hash,
                contract_address=contract_address
            ).transaction_raw()
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
