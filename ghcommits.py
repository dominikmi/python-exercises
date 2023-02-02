import json
import argparse
import requests
import os
from pathlib import Path

# the function takes nested dictionary as argument.

def print_commit_attr(*args):
    index = 0
    number_args=len(args)
    dict_len = len(args[0])
    while (index < dict_len):
        vals = args[0][index]
        line = f'Date: {vals["commit"]["author"]["date"]}, Author: {vals["commit"]["author"]["name"]}, Message: {vals["commit"]["message"]}'
        if number_args == 1: 
            print(line)
        else:
            while (Path(args[1]).is_dir() or Path(args[1]).exists()): 
                break
            else: 
                Path(args[1]).touch()
                Path(args[1]).write_text(line)
        index += 1
    if number_args == 1: 
        print("-" * len(line))
        print(f"Number of commits in the repository: {cliargs.reponame} : {dict_len}")
    else:
        Path(args[1]).write_text("-" * len(line))
        lastline = f"Number of commits in the repository: {cliargs.reponame} : {dict_len}"
        Path(args[1]).write_text(lastline)

# parse arguments

parser = argparse.ArgumentParser(
    prog='commitcheck',
    description='it will list last 30 commits for given repository')

parser.add_argument("-r", "--reponame", type=str, help="Repository Name")
parser.add_argument("-o", "--ownername", type=str, help="Owner Name")
parser.add_argument("-f", "--fileout", type=str, help="Output filename")
cliargs = parser.parse_args()

# Set headers and token

token = os.getenv('GITHUB_API_TOKEN', '...')
url = f"https://api.github.com/repos/{cliargs.ownername}/{cliargs.reponame}/commits"
headers = {'Authorization': f'token {token}'}

# pass the response to json dictionary and run the script passing the dict as an argument to iteration function
# dump the output to file if arg was speficied

if cliargs.fileout: 
    print_commit_attr((requests.get(url, headers=headers).json()), cliargs.fileout)
else: print_commit_attr(requests.get(url, headers=headers).json())