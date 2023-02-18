import json
import argparse
import requests
import os
from pathlib import Path

# the function takes nested dictionary as argument

def print_commit_attr_to_screen(*args):
  for arg in args:
    for vals in arg:
      line = f'Date: {vals["commit"]["author"]["date"]},Author: {vals["commit"]["author"]["name"]},Message: {vals["commit"]["message"]}'
      print(line)
        
# parse arguments, there can be 2 - repo name and owner's name or 3 - + output filename

parser = argparse.ArgumentParser(
    prog='commitcheck',
    description='it will list last 30 commits for given repository')

parser.add_argument("-r", "--reponame", type=str, help="Repository Name")
parser.add_argument("-o", "--ownername", type=str, help="Owner Name")
parser.add_argument("-f", "--fileout", type=str, help="Output filename")
cliargs = parser.parse_args()

# Set headers and token - to be improved

token = os.getenv('GITHUB_API_TOKEN', '...')
url = f"https://api.github.com/repos/{cliargs.ownername}/{cliargs.reponame}/commits"
headers = {'Authorization': f'token {token}'}

output = requests.get(url,headers=headers)

# To fix issue with wiriting to file

if cliargs.fileout:
  Path(cliargs.fileout).touch() 
  Path(cliargs.fileout).write_text(str(print_commit_attr_to_screen(output.json())))
else: 
  print_commit_attr_to_screen(output.json())
