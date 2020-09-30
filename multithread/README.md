# README

## Objective 

Show advantage of parallelization using Wikipedia python lib.
We run 3 versions of the program:

- loop
- map
- parallel map

And show advantages to parallelize http calls.

## Run 

Run client.py with pycharm  

````shell script
script path = C:\[...]\dev_snippets\multithread\client.py
working dir = C:\[...]dev_snippets\multithread
````

or using docker

````shell script
cd ~/dev/dev_snippets/multithread
docker build .
docker build . --no-cache
````

See notes in [README](../README.md#note-on-python-import).

`CI/CD` runs docker-compose [file](../docker-compose.yaml).
In travis if results not visible show raw logs.
It is faster than locally but still big difference between parallel map (2s) and map/loop (13s).

## Notes 

- Reused decorator class for time counter (chrono package)
- Did not use wikipedia library directly: https://github.com/goldsmith/Wikipedia.
We forked it because when doing: 

In pipfile

````shell script
[packages]
wikipedia = "==1.4.0"
````
And python script:

````shell script
import wikipedia
print(mywikipedia.search("covid19"))
print(mywikipedia.summary("Wikipedia"))
````

We had following issue that we initially fixed in pipenv lib dependency.

- [1] Issue with certificate
    - https://stackoverflow.com/questions/15445981/how-do-i-disable-the-security-certificate-check-in-python-requests
    - https://stackoverflow.com/questions/7881122/cxf-restful-client-how-to-do-trust-all-certs/55575644#55575644
    - https://stackoverflow.com/questions/36425540/unable-to-access-wikipedia-api-due-to-ssl-certificate-error
    
- [2] warning removal

````shell script
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
````

- [3] cache disable (`@cache` less needed now as separate file)

We  finally embeds modified lib in the repo.

**Links**:

- https://stackabuse.com/getting-started-with-pythons-wikipedia-api/
- https://towardsdatascience.com/wikipedia-api-for-python-241cfae09f1c
- https://stackoverflow.com/questions/15445981/how-do-i-disable-the-security-certificate-check-in-python-requests -> https://stackoverflow.com/questions/7881122/cxf-restful-client-how-to-do-trust-all-certs/55575644#55575644