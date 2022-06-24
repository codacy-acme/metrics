#!/usr/bin/env python3
import argparse
import requests
import json
import csv


from projects import listRepositories

import datetime
import time

def getPRsGHCloud(organization, repository, providertoken, untilwhen):
    hasNextPage = True
    cursor = 1
    prs = []
    headers = {
        'Accept': 'application/json',
        'Authorization': 'token %s' % providertoken
    }
    while(hasNextPage):
        url = 'https://api.github.com/repos/%s/%s/pulls?per_page=100&page=%s&state=closed' % (
            organization, repository, cursor)
        print(url)
        r = requests.get(url, headers=headers)
        if(r.status_code == 404 or r.status_code == 409):
            break
        response = json.loads(r.text)
        if(not response):
            hasNextPage = False
        else:
            for pr in response:
                if pr['merged_at'] != None:
                    prs.append({
                        'repo': repository,
                        'id': pr['id'],
                        'number': pr['number'],
                        'merged_at': pr['merged_at'],
                        'merged': None,
                        'mergeable_state': None,
                        'mergeable': None,
                        'user': pr['user']['login'],
                        'user_id': pr['user']['id'],
                        'isUpToStandards': None
                    })
                    if datetime.datetime.strptime(pr['merged_at'], "%Y-%m-%dT%H:%M:%SZ") < untilwhen:
                        hasNextPage = False
            cursor += 1
    return prs

def getPrDetails(baseurl, provider, organization, repository, number, token):
    if token == None:
        raise Exception('api-token needs to be defined')
    headers = {
        'Accept': 'application/json',
        'api-token': token
    }
    url = '%s/api/v3/analysis/organizations/%s/%s/repositories/%s/pull-requests/%s' % (
        baseurl, provider, organization, repository, number)
    r = requests.get(url, headers=headers)
    prDetails = json.loads(r.text)
    return prDetails

def main():
    oneYearAgo = datetime.datetime.now() - datetime.timedelta(days=1*365)
    parser = argparse.ArgumentParser(description='Codacy Forced Merges Reporter')
    parser.add_argument('--token', dest='token', default=None,
                        help='the api-token to be used on the REST API', required=True)
    parser.add_argument('--provider-token', dest='providertoken', default=None,
                        help='the provider api token to be used on the REST API', required=True)
    parser.add_argument('--provider', dest='provider',
                        default=None, help='git provider', required=True)
    parser.add_argument('--organization', dest='organization',
                        default=None, help='organization id', required=True)
    parser.add_argument('--baseurl', dest='baseurl', default='https://app.codacy.com',
                        help='codacy server address (ignore if cloud)')
    parser.add_argument('--output', dest='output',
                        default='json', choices=['json', 'csv'])
    args = parser.parse_args()
    
    repos = listRepositories(args.baseurl, args.provider, args.organization, args.token)
    data = []
    for repo in repos:
        prs = getPRsGHCloud(args.organization, repo['repository']['name'], args.providertoken, oneYearAgo)
        for pr in prs:
            prDetails = getPrDetails(args.baseurl, args.provider, args.organization, repo['repository']['name'], pr['number'], args.token)
            pr['isUpToStandards'] = prDetails['isUpToStandards'] if 'isUpToStandards' in prDetails else 'N/A'
            data.append(pr)
            time.sleep(0.5)
    
    if(args.output == 'json'):
        print(json.dumps(data, indent=4))
    elif(args.output == 'csv'):
        with open('output.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['repo', 'number', 'merged_at', 'user', 'user_id', 'UpToStandards'])
            for item in data:
                writer.writerow([item['repo'], item['number'], item['merged_at'], item['user'], item['user_id'], item['isUpToStandards']])
main()