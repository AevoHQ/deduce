"""Aevo Deduce configuration."""

import argparse


def _build_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--vault_ip",
        help="the IP address of Aevo Vault",
        default="http://localhost:3000")

    return parser

ARGS = _build_parser().parse_args()
