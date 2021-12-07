#!/usr/bin/env python3
import argparse
import requests
import json
import csv

from projects import listRepositories

from projects import listRepositories


def getCommitsGHCloud(organization, repository, providertoken):
    hasNextPage = True
    cursor = 1
    commits = []
    headers = {
        'Accept': 'application/json',
        'Authorization': 'token %s' % providertoken
    }
    while(hasNextPage):
        url = 'https://api.github.com/repos/%s/%s/commits?per_page=1000&page=%s' % (
            organization, repository, cursor)
        r = requests.get(url, headers=headers)
        if(r.status_code == 404 or r.status_code == 409):
            break
        response = json.loads(r.text)
        if(not response):
            hasNextPage = False
        else:
            for commit in response:
                if(commit['author'] != None and ('login' in commit['author'])):
                    commits.append({
                        'sha': commit['sha'],
                        'author': commit['author']['login'],
                        'author_id': commit['author']['id'],
                        'delta': {}
                    })
            cursor += 1
    return commits


# TODO: currently only supports GH cloud
def getCommits(provider, organization, repository, providertoken):
    commits = []
    if(provider == 'gh'):
        commits = getCommitsGHCloud(organization, repository, providertoken)
    else:
        print("PROVIDER NOT SUPPORTED YET")
        raise
    return commits


def getDeltaForCommit(baseurl, provider, organization, repository, commitsha, token):
    if token == None:
        raise Exception('api-token needs to be defined')
    headers = {
        'Accept': 'application/json',
        'api-token': token
    }
    url = '%s/api/v3/analysis/organizations/%s/%s/repositories/%s/commits/%s/deltaStatistics' % (
        baseurl, provider, organization, repository, commitsha)
    r = requests.get(url, headers=headers)
    response = json.loads(r.text)
    return response


def topPerformers(commits):
    performers = {}
    for commit in commits:
        if(commit['delta'] == {} or 'error' in commit['delta']):
            continue
        if(commit['delta']['analyzed']):
            if commit['author_id'] not in performers:
                performers[commit['author_id']] = {
                    'author': commit['author'],
                    'totalNewIssues': 0,
                    'totalFixedIssues': 0,
                    'commits': []
                }
            performers[commit['author_id']]['commits'].append({
                'commitUuid': commit['delta']['commitUuid'],
                'newIssues': commit['delta']['newIssues'],
                'fixedIssues': commit['delta']['fixedIssues']
            })
            performers[commit['author_id']
                       ]['totalNewIssues'] += commit['delta']['newIssues']
            performers[commit['author_id']
                       ]['totalFixedIssues'] += commit['delta']['fixedIssues']
    return performers


def main():
    parser = argparse.ArgumentParser(description='Codacy Top Performers')
    parser.add_argument('--token', dest='token', default=None,
                        help='the api-token to be used on the REST API', required=True)
    parser.add_argument('--provider-token', dest='providertoken', default=None,
                        help='the provider api token to be used on the REST API', required=True)
    parser.add_argument('--provider', dest='provider',
                        default=None, help='git provider', required=True)
    parser.add_argument('--organization', dest='organization',
                        default=None, help='organization id', required=True)
    parser.add_argument('--repository', dest='repository',
                        default=None, help='repository id', required=False)
    parser.add_argument('--baseurl', dest='baseurl', default='https://app.codacy.com',
                        help='codacy server address (ignore if cloud)')
    parser.add_argument('--output', dest='output',
                        default='json', choices=['json', 'csv'])
    args = parser.parse_args()
    commits = []
    if(args.repository == None):
        repos = listRepositories(
            args.baseurl, args.provider, args.organization, args.token)
        for repo in repos:
            # print(repo)
            tmpc = getCommits(args.provider, args.organization,
                              repo['repository']['name'], args.providertoken)
            for commit in tmpc:
                commit['delta'] = getDeltaForCommit(
                    args.baseurl, args.provider, args.organization, repo['repository']['name'], commit['sha'], args.token)
            commits += tmpc
    else:
        commits = getCommits(args.provider, args.organization,
                             args.repository, args.providertoken)
        for commit in commits:
            commit['delta'] = getDeltaForCommit(
                args.baseurl, args.provider, args.organization, args.repository, commit['sha'], args.token)
    performers = topPerformers(commits)
    if(args.output == 'json'):
        print(json.dumps(performers, indent=4))
    elif(args.output == 'csv'):
        with open('output.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            for key, item in performers.items():
                writer.writerow(['Introduced', item['author']] + ([i['newIssues'] for i in item['commits']]))
                writer.writerow(['Fixed', item['author']] + ([i['fixedIssues'] for i in item['commits']]))
            


main()
