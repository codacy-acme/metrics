#!/usr/bin/env python3
import argparse
import requests
import json


def main():
    parser = argparse.ArgumentParser(description='Codacy Engine Helper')
    parser.add_argument('--token', dest='token', default=None,
                        help='the api-token to be used on the REST API', required=True)
    parser.add_argument('--provider', dest='provider',
                        default=None, help='git provider', required=True)
    parser.add_argument('--organization', dest='organization',
                        default=None, help='organization id', required=True)
    parser.add_argument('--repository', dest='repository',
                        default=None, help='repository id', required=True)
    parser.add_argument('--baseurl', dest='baseurl', default='https://app.codacy.com',
                        help='codacy server address (ignore if cloud)')
    args = parser.parse_args()


main()