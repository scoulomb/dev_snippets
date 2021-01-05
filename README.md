[![Build Status](https://travis-ci.org/scoulomb/dev_snippets.svg?branch=master)](https://travis-ci.org/scoulomb/dev_snippets)

# dev_snippets

- `serialization`: 
    - Generic serialization of a Python object to a string, with filtering on null value 
    - Deserialize a python dict (<-> serialized string json.load, see test_json_to_object_to_json in test_model) to a python class  
    - In `src/model.py` we are checking if we could have simplified the code proposed in this same class
    - Usage run tests in `tests` folder, it is described in [run tests](#run-python-tests) section.

- `decorators`:
    - Understand decorators

- `mulithread`:
    - Show advantage of using parallel map to parallelize http calls

- `misc` 

- `systemd`:
    - Show usage of system 

- `pipeline`
    - Show usage of pipeline
        
# Run python tests

They are in test folder.
We can configure Pycharm or use Docker

## Pycharm    

Configuring [Pycharm](https://www.jetbrains.com/help/pycharm/pipenv.html#pipenv-existing-project) (in same menu can install without pipenv if issues): 
- Press Ctrl+Alt+S to open the project Settings/Preferences
- In the Settings/Preferences dialog Ctrl+Alt+S, select Project <project name> | Project Interpreter. 
- Click the The Configure project interpreter icon and select Add. 
- In the left-hand pane of this dialog, click Pipenv Environment.
- test OK

## Docker
        
````shell
cd <project> # serialization
docker build .
````   

## Note on python import

````python
from serialization.model import Model
````

In pycharm initial setup it proposed

````python
from serialization.serialization import Model
````

But it would not work with docker (even if copy  `serialization` top folder, cf. multithread where we did it).

Sometimes Pycharm complains by adding yellow in import line, in other project work with moudle, Pycharm behavior is strange

For instance, multithread [client](./multithread/client.py):
````python
from chrono.chrono import with_chrono # <- work in docker, work with pycharm but flagged as red
from multithread.chrono.chrono import with_chrono #  <- does not work in docker, work with pycharm
````

In pycharm ensure template in unittest is correct (close to run > arrow), edit configuration so that we use script path and not module name.
And working directory is `C:\[...]\dev_snippets\serialization` same as docker one.
And add content and source root to Python path.
Similar in [multithread readme](./multithread/README.md).

Docker may require to update pipfile.

## Build all snippets with compose (for CI)

````shell script
# at project root
docker-compose up #(--build)
````

Activate the repo here: https://travis-ci.org/account/repositories

## Remove file from history 

````python
# https://myopswork.com/how-remove-files-completely-from-git-repository-history-47ed3e0c4c35
git filter-branch --index-filter "git rm -rf --cached --ignore-unmatch README.md" HEAD
````

See also repo mgmt 

<!-- and private repo --<