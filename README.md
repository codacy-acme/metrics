# metrics



## Usage

The `requirements.txt` lists all Python libraries that should be installed before running the script:

```bash
pip install -r requirements.txt
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