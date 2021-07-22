#!/usr/bin/env python3

import json
import os

from swap.providers.bitcoin.wallet import Wallet

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_bitcoin_wallet_from_entropy():

    wallet = Wallet(network=_["bitcoin"]["network"])

    wallet.from_entropy(
        entropy=_["bitcoin"]["wallet"]["sender"]["entropy"],
        language=_["bitcoin"]["wallet"]["sender"]["language"],
        passphrase=_["bitcoin"]["wallet"]["sender"]["passphrase"]
    )

    wallet.from_path(
        path=_["bitcoin"]["wallet"]["sender"]["derivation"]["path"]
    )

    assert wallet.entropy() == _["bitcoin"]["wallet"]["sender"]["entropy"]
    assert wallet.mnemonic() == _["bitcoin"]["wallet"]["sender"]["mnemonic"]
    assert wallet.language() == _["bitcoin"]["wallet"]["sender"]["language"]
    assert wallet.passphrase() is None
    assert wallet.seed() == _["bitcoin"]["wallet"]["sender"]["seed"]
    assert wallet.root_xprivate_key() == _["bitcoin"]["wallet"]["sender"]["root_xprivate_key"]
    assert wallet.root_xpublic_key() == _["bitcoin"]["wallet"]["sender"]["root_xpublic_key"]
    assert wallet.xprivate_key() == _["bitcoin"]["wallet"]["sender"]["xprivate_key"]
    assert wallet.xpublic_key() == _["bitcoin"]["wallet"]["sender"]["xpublic_key"]
    assert wallet.uncompressed() == _["bitcoin"]["wallet"]["sender"]["uncompressed"]
    assert wallet.compressed() == _["bitcoin"]["wallet"]["sender"]["compressed"]
    assert wallet.chain_code() == _["bitcoin"]["wallet"]["sender"]["chain_code"]
    assert wallet.private_key() == _["bitcoin"]["wallet"]["sender"]["private_key"]
    assert wallet.public_key() == _["bitcoin"]["wallet"]["sender"]["public_key"]
    assert wallet.wif() == _["bitcoin"]["wallet"]["sender"]["wif"]
    assert wallet.hash() == _["bitcoin"]["wallet"]["sender"]["hash"]
    assert wallet.finger_print() == _["bitcoin"]["wallet"]["sender"]["finger_print"]
    assert wallet.path() == _["bitcoin"]["wallet"]["sender"]["derivation"]["path"]
    assert wallet.address() == _["bitcoin"]["wallet"]["sender"]["address"]

    assert isinstance(wallet.balance(), int)
    assert isinstance(wallet.utxos(), list)


def test_bitcoin_wallet_from_mnemonic():

    wallet = Wallet(network=_["bitcoin"]["network"])

    wallet.from_mnemonic(
        mnemonic=_["bitcoin"]["wallet"]["sender"]["mnemonic"],
        language=_["bitcoin"]["wallet"]["sender"]["language"],
        passphrase=_["bitcoin"]["wallet"]["sender"]["passphrase"]
    )

    wallet.from_path(
        path=_["bitcoin"]["wallet"]["sender"]["derivation"]["path"]
    )

    assert wallet.entropy() == _["bitcoin"]["wallet"]["sender"]["entropy"]
    assert wallet.mnemonic() == _["bitcoin"]["wallet"]["sender"]["mnemonic"]
    assert wallet.language() == _["bitcoin"]["wallet"]["sender"]["language"]
    assert wallet.passphrase() is None
    assert wallet.seed() == _["bitcoin"]["wallet"]["sender"]["seed"]
    assert wallet.root_xprivate_key() == _["bitcoin"]["wallet"]["sender"]["root_xprivate_key"]
    assert wallet.root_xpublic_key() == _["bitcoin"]["wallet"]["sender"]["root_xpublic_key"]
    assert wallet.xprivate_key() == _["bitcoin"]["wallet"]["sender"]["xprivate_key"]
    assert wallet.xpublic_key() == _["bitcoin"]["wallet"]["sender"]["xpublic_key"]
    assert wallet.uncompressed() == _["bitcoin"]["wallet"]["sender"]["uncompressed"]
    assert wallet.compressed() == _["bitcoin"]["wallet"]["sender"]["compressed"]
    assert wallet.chain_code() == _["bitcoin"]["wallet"]["sender"]["chain_code"]
    assert wallet.private_key() == _["bitcoin"]["wallet"]["sender"]["private_key"]
    assert wallet.public_key() == _["bitcoin"]["wallet"]["sender"]["public_key"]
    assert wallet.wif() == _["bitcoin"]["wallet"]["sender"]["wif"]
    assert wallet.hash() == _["bitcoin"]["wallet"]["sender"]["hash"]
    assert wallet.finger_print() == _["bitcoin"]["wallet"]["sender"]["finger_print"]
    assert wallet.path() == _["bitcoin"]["wallet"]["sender"]["derivation"]["path"]
    assert wallet.address() == _["bitcoin"]["wallet"]["sender"]["address"]

    # assert isinstance(wallet.balance(), int)
    # assert isinstance(wallet.utxos(), list)


def test_bitcoin_wallet_from_seed():

    wallet = Wallet(network=_["bitcoin"]["network"])

    wallet.from_seed(
        seed=_["bitcoin"]["wallet"]["recipient"]["seed"]
    )

    wallet.from_path(
        path=_["bitcoin"]["wallet"]["recipient"]["derivation"]["path"]
    )

    assert wallet.entropy() is None
    assert wallet.mnemonic() is None
    assert wallet.language() is None
    assert wallet.passphrase() is None
    assert wallet.seed() == _["bitcoin"]["wallet"]["recipient"]["seed"]
    assert wallet.root_xprivate_key() == _["bitcoin"]["wallet"]["recipient"]["root_xprivate_key"]
    assert wallet.root_xpublic_key() == _["bitcoin"]["wallet"]["recipient"]["root_xpublic_key"]
    assert wallet.xprivate_key() == _["bitcoin"]["wallet"]["recipient"]["xprivate_key"]
    assert wallet.xpublic_key() == _["bitcoin"]["wallet"]["recipient"]["xpublic_key"]
    assert wallet.uncompressed() == _["bitcoin"]["wallet"]["recipient"]["uncompressed"]
    assert wallet.compressed() == _["bitcoin"]["wallet"]["recipient"]["compressed"]
    assert wallet.chain_code() == _["bitcoin"]["wallet"]["recipient"]["chain_code"]
    assert wallet.private_key() == _["bitcoin"]["wallet"]["recipient"]["private_key"]
    assert wallet.public_key() == _["bitcoin"]["wallet"]["recipient"]["public_key"]
    assert wallet.wif() == _["bitcoin"]["wallet"]["recipient"]["wif"]
    assert wallet.hash() == _["bitcoin"]["wallet"]["recipient"]["hash"]
    assert wallet.finger_print() == _["bitcoin"]["wallet"]["recipient"]["finger_print"]
    assert wallet.path() == _["bitcoin"]["wallet"]["recipient"]["derivation"]["path"]
    assert wallet.address() == _["bitcoin"]["wallet"]["recipient"]["address"]

    # assert isinstance(wallet.balance(), int)
    # assert isinstance(wallet.utxos(), list)


def test_bitcoin_wallet_from_root_xprivate_key():

    wallet = Wallet(network=_["bitcoin"]["network"])

    wallet.from_root_xprivate_key(
        xprivate_key=_["bitcoin"]["wallet"]["sender"]["root_xprivate_key"]
    )

    wallet.from_path(
        path=_["bitcoin"]["wallet"]["sender"]["derivation"]["path"]
    )

    assert wallet.entropy() is None
    assert wallet.mnemonic() is None
    assert wallet.language() is None
    assert wallet.passphrase() is None
    assert wallet.seed() is None
    assert wallet.root_xprivate_key() == _["bitcoin"]["wallet"]["sender"]["root_xprivate_key"]
    assert wallet.root_xpublic_key() == _["bitcoin"]["wallet"]["sender"]["root_xpublic_key"]
    assert wallet.xprivate_key() == _["bitcoin"]["wallet"]["sender"]["xprivate_key"]
    assert wallet.xpublic_key() == _["bitcoin"]["wallet"]["sender"]["xpublic_key"]
    assert wallet.uncompressed() == _["bitcoin"]["wallet"]["sender"]["uncompressed"]
    assert wallet.compressed() == _["bitcoin"]["wallet"]["sender"]["compressed"]
    assert wallet.chain_code() == _["bitcoin"]["wallet"]["sender"]["chain_code"]
    assert wallet.private_key() == _["bitcoin"]["wallet"]["sender"]["private_key"]
    assert wallet.public_key() == _["bitcoin"]["wallet"]["sender"]["public_key"]
    assert wallet.wif() == _["bitcoin"]["wallet"]["sender"]["wif"]
    assert wallet.hash() == _["bitcoin"]["wallet"]["sender"]["hash"]
    assert wallet.finger_print() == _["bitcoin"]["wallet"]["sender"]["finger_print"]
    assert wallet.path() == _["bitcoin"]["wallet"]["sender"]["derivation"]["path"]
    assert wallet.address() == _["bitcoin"]["wallet"]["sender"]["address"]

    # assert isinstance(wallet.balance(), int)
    # assert isinstance(wallet.utxos(), list)


def test_bitcoin_wallet_from_xprivate_key():

    wallet = Wallet(network=_["bitcoin"]["network"])

    wallet.from_xprivate_key(
        xprivate_key=_["bitcoin"]["wallet"]["recipient"]["xprivate_key"]
    )

    assert wallet.entropy() is None
    assert wallet.mnemonic() is None
    assert wallet.language() is None
    assert wallet.passphrase() is None
    assert wallet.seed() is None
    assert wallet.root_xprivate_key() is None
    assert wallet.root_xpublic_key() is None
    assert wallet.xprivate_key() == _["bitcoin"]["wallet"]["recipient"]["xprivate_key"]
    assert wallet.xpublic_key() == _["bitcoin"]["wallet"]["recipient"]["xpublic_key"]
    assert wallet.uncompressed() == _["bitcoin"]["wallet"]["recipient"]["uncompressed"]
    assert wallet.compressed() == _["bitcoin"]["wallet"]["recipient"]["compressed"]
    assert wallet.chain_code() == _["bitcoin"]["wallet"]["recipient"]["chain_code"]
    assert wallet.private_key() == _["bitcoin"]["wallet"]["recipient"]["private_key"]
    assert wallet.public_key() == _["bitcoin"]["wallet"]["recipient"]["public_key"]
    assert wallet.wif() == _["bitcoin"]["wallet"]["recipient"]["wif"]
    assert wallet.hash() == _["bitcoin"]["wallet"]["recipient"]["hash"]
    assert wallet.finger_print() == _["bitcoin"]["wallet"]["recipient"]["finger_print"]
    assert wallet.path() is None
    assert wallet.address() == _["bitcoin"]["wallet"]["recipient"]["address"]

    # assert isinstance(wallet.balance(), int)
    # assert isinstance(wallet.utxos(), list)


def test_bitcoin_wallet_from_private_key():

    wallet = Wallet(network=_["bitcoin"]["network"])

    wallet.from_private_key(
        private_key=_["bitcoin"]["wallet"]["sender"]["private_key"]
    )

    assert wallet.entropy() is None
    assert wallet.mnemonic() is None
    assert wallet.language() is None
    assert wallet.passphrase() is None
    assert wallet.seed() is None
    assert wallet.root_xprivate_key() is None
    assert wallet.root_xpublic_key() is None
    assert wallet.xprivate_key() is None
    assert wallet.xpublic_key() is None
    assert wallet.uncompressed() == _["bitcoin"]["wallet"]["sender"]["uncompressed"]
    assert wallet.compressed() == _["bitcoin"]["wallet"]["sender"]["compressed"]
    assert wallet.chain_code() is None
    assert wallet.private_key() == _["bitcoin"]["wallet"]["sender"]["private_key"]
    assert wallet.public_key() == _["bitcoin"]["wallet"]["sender"]["public_key"]
    assert wallet.wif() == _["bitcoin"]["wallet"]["sender"]["wif"]
    assert wallet.hash() == _["bitcoin"]["wallet"]["sender"]["hash"]
    assert wallet.finger_print() == _["bitcoin"]["wallet"]["sender"]["finger_print"]
    assert wallet.path() is None
    assert wallet.address() == _["bitcoin"]["wallet"]["sender"]["address"]

    # assert isinstance(wallet.balance(), int)
    # assert isinstance(wallet.utxos(), list)
