#!/usr/bin/env python3

from base64 import b64decode
from pybytom.utils import is_address as btm_is_address
from typing import Optional, Union

import requests
import json
import datetime

from ...utils import clean_transaction_raw
from ...exceptions import (
    NetworkError, APIError, TransactionRawError, SymbolError, AddressError
)
from ..config import vapor

# Vapor config
config: dict = vapor()


def amount_converter(amount: Union[int, float], symbol: str = "NEU2BTM") -> Union[int, float]:
    """
    Vapor amount converter.

    :param amount: Vapor amount.
    :type amount: int, float
    :param symbol: Vapor symbol, default to NEU2BTM.
    :type symbol: str

    :returns: int, float -- BTM asset amount.

    >>> from swap.providers.vapor.utils import amount_converter
    >>> amount_converter(amount=10_000_000, symbol="NEU2BTM")
    0.1
    """

    if symbol not in ["BTM2mBTM", "BTM2NEU", "mBTM2BTM", "mBTM2NEU", "NEU2BTM", "NEU2mBTM"]:
        raise SymbolError(f"Invalid '{symbol}' symbol/type",
                          "choose only 'BTM2mBTM', 'BTM2NEU', 'mBTM2BTM', 'mBTM2NEU', 'NEU2BTM' or 'NEU2mBTM' symbols.")

    # Constant values
    BTM, mBTM, NEU = (1, 1000, 100_000_000)

    if symbol == "BTM2mBTM":
        return float((amount * mBTM) / BTM)
    elif symbol == "BTM2NEU":
        return int((amount * NEU) / BTM)
    elif symbol == "mBTM2BTM":
        return float((amount * BTM) / mBTM)
    elif symbol == "mBTM2NEU":
        return int((amount * NEU) / mBTM)
    elif symbol == "NEU2BTM":
        return float((amount * BTM) / NEU)
    elif symbol == "NEU2mBTM":
        return int((amount * mBTM) / NEU)


def is_network(network: str) -> bool:
    """
    Check Vapor network.

    :param network: Vapor network.
    :type network: str

    :returns: bool -- Vapor valid/invalid network.

    >>> from swap.providers.vapor.utils import is_network
    >>> is_network(network="solonet")
    True
    """

    if not isinstance(network, str):
        raise TypeError(f"Network must be str, not '{type(network)}' type.")
    return network in ["mainnet", "solonet", "testnet"]


def is_address(address: str, network: Optional[str] = None) -> bool:
    """
    Check Vapor address.

    :param address: Vapor address.
    :type address: str
    :param network: Vapor network, defaults to None.
    :type network: str

    :returns: bool -- Vapor valid/invalid address.

    >>> from swap.providers.vapor.utils import is_address
    >>> is_address(address="vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag", network="mainnet")
    True
    """

    if not isinstance(address, str):
        raise TypeError(f"Address must be str, not '{type(address)}' type.")
    if network is None:
        return btm_is_address(address=address, vapor=True)
    elif not is_network(network=network):
        raise NetworkError(f"Invalid Vapor '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")
    return btm_is_address(address=address, network=network, vapor=True)


def is_transaction_raw(transaction_raw: str) -> bool:
    """
    Check Vapor transaction raw.

    :param transaction_raw: Vapor transaction raw.
    :type transaction_raw: str

    :returns: bool -- Vapor valid/invalid transaction raw.

    >>> from swap.providers.vapor.utils import is_transaction_raw
    >>> transaction_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcWU5MHFqdDl3NG04cnQzdG51dTBwenAyNGRrZmZlbHlzOHpjd3llIiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkMzA1YTI4ZDhkMzRiNDBjNjU5MzY4MTBmOWU5YzFmOGJjOWM3OTNlYzJlNzJjNzBmOTIwM2ZiYmViMGE1NmRiOWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGFkZTIwNDAxMDExNjAwMTQwZTQzYTkyYTllOGFjYTc4OGViMTU1MWMzMTY0NDhjMmUzZjc4MjE1MDEwMDAxNWYwMTVkMjAyZmQyNTU3YjY3ZjFkZjhiOGFjZWYwNjZmNWQ0NmE4NTAwODE0MzliNDE5MzI1ZDU1ZGJkOTM0MWUxMWFjNGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MDg0YWY1ZjAxMDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMjIwMTIwNTk5MDdmZGFkMGZmOTVmZWJhNDNhZWYzN2QyZTU1YzU3YjZlMTg2Y2QzYWQxN2M4M2U2YzgwYzY1ODIxOGI2NTAyMDEzYWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmUwOTQ5MDY0MDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMDAiLCAiaGFzaCI6ICI3NzlmYzliOWNhNGRiMTVkNDFhYzgwNDNlZDRlNDFkYjg4NDU2ZjA1YzljZmJhMDQ5MzYyZWNlZmQ2MjY3ZmMzIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjMzZThkYThjZThlZjEzZmI0OTM4YTM3NGFlYTM2NjRlNGNkMmNkMDBmZGQ5ZDI5ODU5M2JkYmQ4NzJkNjZiODgiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbIjc1ZTg3Yzc5MzNiNGRjNGE4N2UwNmZlZDMyM2U4NDI1ZTU0YTQ5NGZmODBkYzdmOGM0NTUyY2RiMGE2YmM3NGEiXSwgInB1YmxpY19rZXkiOiAiNTk5MDdmZGFkMGZmOTVmZWJhNDNhZWYzN2QyZTU1YzU3YjZlMTg2Y2QzYWQxN2M4M2U2YzgwYzY1ODIxOGI2NSIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX2NsYWltX3Vuc2lnbmVkIn0"
    >>> is_transaction_raw(transaction_raw=transaction_raw)
    True
    """

    if not isinstance(transaction_raw, str):
        raise TypeError(f"Transaction raw must be str, not '{type(transaction_raw)}' type.")
    
    try:
        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())
        return loaded_transaction_raw["type"] in [
            "vapor_fund_unsigned", "vapor_fund_signed",
            "vapor_claim_unsigned", "vapor_claim_signed",
            "vapor_refund_unsigned", "vapor_refund_signed"
        ]
    except:
        return False


def decode_transaction_raw(transaction_raw: str, headers: dict = config["headers"],
                           timeout: int = config["timeout"]) -> dict:
    """
    Decode Vapor transaction raw.

    :param transaction_raw: Vapor transaction raw.
    :type transaction_raw: str
    :param headers: Request headers, default to common headers.
    :type headers: dict
    :param timeout: Request timeout, default to 60.
    :type timeout: int

    :returns: dict -- Decoded Vapor transaction raw.

    >>> from swap.providers.vapor.utils import decode_transaction_raw
    >>> transaction_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcWU5MHFqdDl3NG04cnQzdG51dTBwenAyNGRrZmZlbHlzOHpjd3llIiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkMzA1YTI4ZDhkMzRiNDBjNjU5MzY4MTBmOWU5YzFmOGJjOWM3OTNlYzJlNzJjNzBmOTIwM2ZiYmViMGE1NmRiOWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGFkZTIwNDAxMDExNjAwMTQwZTQzYTkyYTllOGFjYTc4OGViMTU1MWMzMTY0NDhjMmUzZjc4MjE1MDEwMDAxNWYwMTVkMjAyZmQyNTU3YjY3ZjFkZjhiOGFjZWYwNjZmNWQ0NmE4NTAwODE0MzliNDE5MzI1ZDU1ZGJkOTM0MWUxMWFjNGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MDg0YWY1ZjAxMDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMjIwMTIwNTk5MDdmZGFkMGZmOTVmZWJhNDNhZWYzN2QyZTU1YzU3YjZlMTg2Y2QzYWQxN2M4M2U2YzgwYzY1ODIxOGI2NTAyMDEzYWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmUwOTQ5MDY0MDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMDAiLCAiaGFzaCI6ICI3NzlmYzliOWNhNGRiMTVkNDFhYzgwNDNlZDRlNDFkYjg4NDU2ZjA1YzljZmJhMDQ5MzYyZWNlZmQ2MjY3ZmMzIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjMzZThkYThjZThlZjEzZmI0OTM4YTM3NGFlYTM2NjRlNGNkMmNkMDBmZGQ5ZDI5ODU5M2JkYmQ4NzJkNjZiODgiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbIjc1ZTg3Yzc5MzNiNGRjNGE4N2UwNmZlZDMyM2U4NDI1ZTU0YTQ5NGZmODBkYzdmOGM0NTUyY2RiMGE2YmM3NGEiXSwgInB1YmxpY19rZXkiOiAiNTk5MDdmZGFkMGZmOTVmZWJhNDNhZWYzN2QyZTU1YzU3YjZlMTg2Y2QzYWQxN2M4M2U2YzgwYzY1ODIxOGI2NSIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX2NsYWltX3Vuc2lnbmVkIn0"
    >>> decode_transaction_raw(transaction_raw=transaction_raw)
    {'fee': ..., 'type': '...', 'address': '...', 'transaction': {...}, 'unsigned_datas': [...], 'signatures': [...], 'network': '...'}
    """
    
    if not is_transaction_raw(transaction_raw=transaction_raw):
        raise TransactionRawError("Invalid Vapor transaction raw.")

    transaction_raw = clean_transaction_raw(transaction_raw)
    decoded_transaction_raw = b64decode(transaction_raw.encode())
    loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

    url = f"{config[loaded_transaction_raw['network']]['vapor-core']}/decode-raw-transaction"
    data = dict(raw_transaction=loaded_transaction_raw["raw"])
    response = requests.post(
        url=url, data=json.dumps(data), headers=headers, timeout=timeout
    )
    response_json = response.json()
    if response.status_code == 400:
        raise APIError(response_json["msg"], response_json["code"])

    return dict(
        fee=loaded_transaction_raw["fee"],
        address=loaded_transaction_raw["address"],
        type=loaded_transaction_raw["type"],
        tx=response_json["data"],
        unsigned_datas=loaded_transaction_raw["unsigned_datas"],
        signatures=loaded_transaction_raw["signatures"],
        network=loaded_transaction_raw["network"]
    )


def submit_transaction_raw(transaction_raw: str, headers: dict = config["headers"],
                           timeout: int = config["timeout"]) -> dict:
    """
    Submit Vapor transaction raw.

    :param transaction_raw: Vapor transaction raw.
    :type transaction_raw: str
    :param headers: Request headers, default to common headers.
    :type headers: dict
    :param timeout: Request timeout, default to 60.
    :type timeout: int

    :returns: dict -- Vapor submitted transaction id, fee, type and date.

    >>> from swap.providers.vapor.utils import submit_transaction_raw
    >>> transaction_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcWU5MHFqdDl3NG04cnQzdG51dTBwenAyNGRrZmZlbHlzOHpjd3llIiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkMzA1YTI4ZDhkMzRiNDBjNjU5MzY4MTBmOWU5YzFmOGJjOWM3OTNlYzJlNzJjNzBmOTIwM2ZiYmViMGE1NmRiOWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGFkZTIwNDAxMDExNjAwMTQwZTQzYTkyYTllOGFjYTc4OGViMTU1MWMzMTY0NDhjMmUzZjc4MjE1MDEwMDAxNWYwMTVkMjAyZmQyNTU3YjY3ZjFkZjhiOGFjZWYwNjZmNWQ0NmE4NTAwODE0MzliNDE5MzI1ZDU1ZGJkOTM0MWUxMWFjNGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MDg0YWY1ZjAxMDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMjIwMTIwNTk5MDdmZGFkMGZmOTVmZWJhNDNhZWYzN2QyZTU1YzU3YjZlMTg2Y2QzYWQxN2M4M2U2YzgwYzY1ODIxOGI2NTAyMDEzYWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmUwOTQ5MDY0MDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMDAiLCAiaGFzaCI6ICI3NzlmYzliOWNhNGRiMTVkNDFhYzgwNDNlZDRlNDFkYjg4NDU2ZjA1YzljZmJhMDQ5MzYyZWNlZmQ2MjY3ZmMzIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjMzZThkYThjZThlZjEzZmI0OTM4YTM3NGFlYTM2NjRlNGNkMmNkMDBmZGQ5ZDI5ODU5M2JkYmQ4NzJkNjZiODgiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbIjc1ZTg3Yzc5MzNiNGRjNGE4N2UwNmZlZDMyM2U4NDI1ZTU0YTQ5NGZmODBkYzdmOGM0NTUyY2RiMGE2YmM3NGEiXSwgInB1YmxpY19rZXkiOiAiNTk5MDdmZGFkMGZmOTVmZWJhNDNhZWYzN2QyZTU1YzU3YjZlMTg2Y2QzYWQxN2M4M2U2YzgwYzY1ODIxOGI2NSIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX2NsYWltX3Vuc2lnbmVkIn0"
    >>> submit_transaction_raw(transaction_raw=transaction_raw)
    {'fee': ..., 'type': '...', 'transaction_id': '...', 'network': '...', 'date': '...'}
    """

    if not is_transaction_raw(transaction_raw=transaction_raw):
        raise TransactionRawError("Invalid Vapor transaction raw.")

    transaction_raw = clean_transaction_raw(transaction_raw)
    decoded_transaction_raw = b64decode(transaction_raw.encode())
    loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

    url = f"{config[loaded_transaction_raw['network']]['blockcenter']}/merchant/submit-payment"
    data = dict(raw_transaction=loaded_transaction_raw["raw"], signatures=loaded_transaction_raw["signatures"])
    params = dict(address=loaded_transaction_raw["address"])
    response = requests.post(
        url=url, data=json.dumps(data), params=params, headers=headers, timeout=timeout
    )
    response_json = response.json()
    if response_json["code"] != 200 and response_json["code"] != 200:
        raise APIError(response_json["msg"], response_json["code"])

    return dict(
        fee=loaded_transaction_raw["fee"],
        type=loaded_transaction_raw["type"],
        transaction_id=response_json["data"]["tx_hash"],
        network=loaded_transaction_raw["network"],
        date=str(datetime.datetime.utcnow())
    )


def get_address_type(address: str) -> Optional[str]:
    """
    Get Vapor address type.

    :param address: Vapor address.
    :type address: str

    :returns: str -- Vapor address type (P2WPKH, P2WSH).

    >>> from swap.providers.vapor.utils import get_address_type
    >>> get_address_type(address="vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag")
    "p2wpkh"
    """

    if not is_address(address=address):
        raise AddressError(f"Invalid Vapor '{address}' address.")

    if len(address) == 42:
        return "p2wpkh"
    elif len(address) == 62:
        return "p2wsh"
    else:
        return None