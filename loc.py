#!/usr/bin/env python3
import argparse
import requests
import json
import time
import csv


# - Per project, by commit
# - Total lines of code
# - Time period one year min

def overallReport(baseurl, provider, organization, repository, token):
    if token == None:
        raise Exception('api-token needs to be defined')
    headers = {
        'Accept': 'application/json',
        'api-token': token
    }
    hasNextPage = True
    cursor = 1
    files = []
    while(hasNextPage):
        url = '%s/api/v3/organizations/%s/%s/repositories/%s/files?limit=100&cursor=%s' % (
            baseurl, provider, organization, repository, cursor)
        r = requests.get(url, headers=headers)
        response = json.loads(r.text)
        files += response['data']
        if('pagination' in response and 'cursor' in response['pagination']):
            cursor = response['pagination']['cursor']
        else:
            hasNextPage = False
    totalLoc = sum(item['linesOfCode'] for item in files)
    print('Total LoC is: %s' % totalLoc)
    return totalLoc


def timeReport(baseurl, provider, organization, repository, days, token):
    if token == None:
        raise Exception('api-token needs to be defined')
    headers = {
        'Accept': 'application/json',
        'api-token': token
    }
    commits = []
    url = '%s/api/v3/analysis/organizations/%s/%s/repositories/%s/commit-statistics?days=%s' % (
        baseurl, provider, organization, repository, days)
    r = requests.get(url, headers=headers)
    response = json.loads(r.text)
    for commit in response['data']:
        commits.append({
            'commitShortUUID': commit['commitShortUUID'],
            'commitTimestamp': commit['commitTimestamp'],
            'numberLoc': commit['numberLoc'],
            'numberIssues': commit['numberIssues'],
            'numberComplexFiles': commit['numberComplexFiles'],
            'numberDuplicatedLines': commit['numberDuplicatedLines'],
            'numberFilesUncovered': commit['numberFilesUncovered']

        })
    print(commits)
    return commits

def main():
    print('Codacy - LoC Metrics')
    parser = argparse.ArgumentParser(description='Codacy LoC Metrics')
    parser.add_argument('--token', dest='token', default=None,
                        help='the api-token to be used on the REST API', required=True)
    parser.add_argument('--provider', dest='provider',
                        default=None, help='git provider', required=True)
    parser.add_argument('--organization', dest='organization',
                        default=None, help='organization name', required=True)
    parser.add_argument('--repository', dest='repository',
                        default=None, help='repository name', required=True)
    parser.add_argument('--baseurl', dest='baseurl', default='https://app.codacy.com',
                        help='codacy server address (ignore if cloud)')
    parser.add_argument('--action', dest='action',
                        default='overall', choices=['overall', 'time'])
    parser.add_argument('--days', dest='days',
                        default='30')
    args = parser.parse_args()
    if(args.action == 'overall'):
        locReport = overallReport(
            args.baseurl, args.provider, args.organization, args.repository, args.token)
    elif(args.action == 'time'):
        locReport = timeReport(
            args.baseurl, args.provider, args.organization, args.repository, args.days, args.token)


main()
