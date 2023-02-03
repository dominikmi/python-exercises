# python-exercises

Testing and upskilling in Python

## Working environment

1. Install globally `virtualenv`
2. run `source env/bin/activate` in the working directory
3. If you use VSC pick python in your local directory (set by virtualenv)
4. Install necessary libs using `pip`
5. When finished, run `deactivate`

## Exercises

1. `ghcommits.py` takes history of commits for given user's name and repo.

Install required modules within your venv with `pip install -r requirements.txt `

```txt
usage: ghcommits [-h] [-r REPONAME] [-o OWNERNAME] [-f FILEOUT]

it will list last 30 commits for given repository

options:
  -h, --help            show this help message and exit
  -r REPONAME, --reponame REPONAME
                        Repository Name
  -o OWNERNAME, --ownername OWNERNAME
                        Owner Name
  -f FILEOUT, --fileout FILEOUT
                        Output filename
```
