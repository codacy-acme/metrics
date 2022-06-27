# metrics



## Usage

The `requirements.txt` lists all Python libraries that should be installed before running the script:

```bash
pip3 install -r requirements.txt
```


### LoC
Returns the numer of Lines of Code per project (overall) or over time (time) for a specific repository

    usage: python3 loc.py [-h] --token TOKEN --provider PROVIDER --organization ORGANIZATION --repository REPOSITORY [--baseurl BASEURL] [--action {overall,time}] [--days DAYS]

    Codacy LoC Metrics

    optional arguments:
    -h, --help            show this help message and exit
    --token TOKEN         the api-token to be used on the REST API
    --provider PROVIDER   git provider
    --organization ORGANIZATION
                            organization name
    --repository REPOSITORY
                            repository name
    --baseurl BASEURL     codacy server address (ignore if cloud)
    --action {overall,time}
    --days DAYS

### Codacy Top Performers
Calculates the number of introduced and fixed issues by contributor. Currently only working for GitHub cloud

    usage: python3 topperformers.py [-h] --token TOKEN --provider-token PROVIDERTOKEN --provider PROVIDER --organization ORGANIZATION --repository REPOSITORY --output (json|csv) [--baseurl BASEURL] 
    
    Codacy Top Performers
    
    Arguments:
    -h, --help            show this help message and exit
    --token TOKEN         the api-token to be used on the REST API
    --provider-token PROVIDERTOKEN
                            the provider api token to be used on the REST API
    --provider PROVIDER   git provider
    --organization ORGANIZATION
                            organization id
    --repository REPOSITORY
                            repository id
    --baseurl BASEURL     codacy server address (ignore if cloud)


### Codacy Org Metrics
Lists Open PRs, Issues and Quality Gate for all repos on an org

    usage: python3 orgreport.py [-h] --token TOKEN --provider PROVIDER --organization ORGANIZATION [--baseurl BASEURL]

    Codacy Org Metrics

    Arguments:
    -h, --help            show this help message and exit
    --token TOKEN         the api-token to be used on the REST API
    --provider PROVIDER   git provider
    --organization ORGANIZATION
                        organization id
    --baseurl BASEURL     codacy server address (ignore if cloud)


### Codacy Forced Merges Reporter
Lists Closed PRs with a reference if it was up to standards when being merged

    usage: forcemergedprs.py [-h] --token TOKEN --provider-token PROVIDERTOKEN --provider PROVIDER --organization ORGANIZATION
                         [--baseurl BASEURL] [--output {json,csv}]

    Codacy Forced Merges Reporter

    optional arguments:
    -h, --help            show this help message and exit
    --token TOKEN         the api-token to be used on the REST API
    --provider-token PROVIDERTOKEN
                            the provider api token to be used on the REST API
    --provider PROVIDER   git provider
    --organization ORGANIZATION
                            organization id
    --baseurl BASEURL     codacy server address (ignore if cloud)
    --output {json,csv}

## Most Common Issues

Lists the most common issues found on a repo or on an organization

    usage: commonissues.py [-h] --token TOKEN --provider-token PROVIDERTOKEN
                        --provider PROVIDER --organization ORGANIZATION
                        [--repository REPOSITORY] [--baseurl BASEURL]
                        [--output {json,csv}]


    optional arguments:
    -h, --help            show this help message and exit
    --token TOKEN         the api-token to be used on the REST API
    --provider-token PROVIDERTOKEN
                            the provider api token to be used on the REST API
    --provider PROVIDER   git provider
    --organization ORGANIZATION
                            organization id
    --repository REPOSITORY
                            repository id
    --baseurl BASEURL     codacy server address (ignore if cloud)
    --output {json,csv}
