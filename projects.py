#!/usr/bin/env python3
import argparse
import requests
import json
import time
import csv

# TODO: paginate instead of requesting 10000 repos


def listRepositories(baseurl, provider, organization, token):
    if token == None:
        raise Exception('api-token needs to be defined')
    headers = {
        'Accept': 'application/json',
        'api-token': token
    }
    url = '%s/api/v3/analysis/organizations/%s/%s/repositories?limit=10000' % (
        baseurl, provider, organization)
    r = requests.get(url, headers=headers)
    repositories = json.loads(r.text)
    return repositories['data']


def listPullRequests(baseurl, provider, organization, repository, token):
    if token == None:
        raise Exception('api-token needs to be defined')
    headers = {
        'Accept': 'application/json',
        'api-token': token
    }
    url = '%s/api/v3/analysis/organizations/%s/%s/repositories/%s/pull-requests?limit=10000' % (
        baseurl, provider, organization, repository)
    r = requests.get(url, headers=headers)
    repositories = json.loads(r.text)
    return repositories['data']

def listIssuesCategoryOverviews(baseurl, provider, organization, repository, token):
    if token == None:
        raise Exception('api-token needs to be defined')
    headers = {
        'Accept': 'application/json',
        'api-token': token
    }
    url = '%s/api/v3/analysis/organizations/%s/%s/repositories/%s/category-overviews' % (
        baseurl, provider, organization, repository)
    r = requests.get(url, headers=headers)
    repositories = json.loads(r.text)
    return repositories['data']

def listPRQualitySettings(baseurl, provider, organization, repository, token):
    if token == None:
        raise Exception('api-token needs to be defined')
    headers = {
        'Accept': 'application/json',
        'api-token': token
    }
    url = '%s/api/v3/organizations/%s/%s/repositories/%s/settings/quality/pull-requests' % (
        baseurl, provider, organization, repository)
    r = requests.get(url, headers=headers)
    repositories = json.loads(r.text)
    return repositories['data']

def main():
    parser = argparse.ArgumentParser(description='Codacy Engine Helper')
    parser.add_argument('--token', dest='token', default=None,
                        help='the api-token to be used on the REST API', required=True)
    parser.add_argument('--provider', dest='provider',
                        default=None, help='git provider', required=True)
    parser.add_argument('--organization', dest='organization',
                        default=None, help='organization id', required=True)
    parser.add_argument('--baseurl', dest='baseurl', default='https://app.codacy.com',
                        help='codacy server address (ignore if cloud)')
    args = parser.parse_args()

    repositories = listRepositories(
        args.baseurl, args.provider, args.organization, args.token)
    for repo in repositories:
        print('[Repository %s] %s' % (repo['repository']['repositoryId'], repo['repository']['name']))


#main()
