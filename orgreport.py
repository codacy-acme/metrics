#!/usr/bin/env python3
import argparse
import requests
import json
from tabulate import tabulate

from projects import listIssuesCategoryOverviews, listPRQualitySettings, listRepositories, listPullRequests


def main():
    parser = argparse.ArgumentParser(description='Codacy Top Performers')
    parser.add_argument('--token', dest='token', default=None,
                        help='the api-token to be used on the REST API', required=True)
    parser.add_argument('--provider', dest='provider',
                        default=None, help='git provider', required=True)
    parser.add_argument('--organization', dest='organization',
                        default=None, help='organization id', required=True)
    parser.add_argument('--baseurl', dest='baseurl', default='https://app.codacy.com',
                        help='codacy server address (ignore if cloud)')
    args = parser.parse_args()

    results = []
    results.append(
        {
            'name': 'Repo Name', 
            'blockedPRs': '# Blocked PRs', 
            'qualityGate': 'Quality Settings', 
            'issuesFound': 'Issues Found'
        }
    )
    repos = listRepositories(args.baseurl, args.provider,
                             args.organization, args.token)
    for repo in repos:
        prs = listPullRequests(args.baseurl, args.provider,
                               args.organization, repo['repository']['name'], args.token)
        blockedPRs = sum(map(lambda pr : 'isUpToStandards' in pr and pr['isUpToStandards'] == False, prs))
        issuesDrillDown = listIssuesCategoryOverviews(args.baseurl, args.provider,
                               args.organization, repo['repository']['name'], args.token)
        issues = sum(map(lambda idd : idd['totalResults'], issuesDrillDown))
        qualityGate = listPRQualitySettings(args.baseurl, args.provider,
                               args.organization, repo['repository']['name'], args.token)
        qgStatus = 'DISABLED'
        if qualityGate != {}:
            qgStatus = 'ENABLED'
        results.append({
            'name': repo['repository']['name'],
            'blockedPRs': blockedPRs,
            'qualityGate': qgStatus,
            'issuesFound': issues
        })
    print(tabulate(results, headers='firstrow'))


main()
