import json
import argparse
import requests
import os
from dotenv import load_dotenv
from pathlib import Path

# the function takes nested dictionary as argument.

def print_commit_attr(commitjson):
    index = 0
    dict_len = len(commitjson)
    while (index < dict_len):
        vals = commitjson[index]
        line = f'Date: {vals["commit"]["author"]["date"]}, Author: {vals["commit"]["author"]["name"]}, Message: {vals["commit"]["message"]}'
        print(line)
        index += 1
    print("-" * len(line))
    print(f"Number of commits in the repository: {args.reponame} : {dict_len}")

# parse arguments

parser = argparse.ArgumentParser(
    prog='commitcheck',
    description='List out last 30 commits for given repository')

parser.add_argument("-r", "--reponame", type=str, help="Repository Name")
parser.add_argument("-o", "--ownername", type=str, help="Owner Name")
args = parser.parse_args()

# Set headers and token

load_dotenv()

token = os.getenv('GITHUB_API_TOKEN', '...')
url = f"https://api.github.com/repos/{args.ownername}/{args.reponame}/commits"
headers = {'Authorization': f'token {token}'}

# pass the response to json dictionary and run the script passing the dict as an argument to iteration function

print_commit_attr(requests.get(url, headers=headers).json())
