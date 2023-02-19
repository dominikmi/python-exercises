import json
import argparse
import requests
import os
from dotenv import load_dotenv
import contextlib

# the function takes nested dictionary as argument

def print_commit_attr_to_screen(*args):
  for arg in args:
    for vals in arg:
      line = f'Date: {vals["commit"]["author"]["date"]},Author: {vals["commit"]["author"]["name"]},Message: {vals["commit"]["message"]}'
      print(line)

def print_commit_attr_to_file(filename,dict):
  with open(filename, "w") as external_file:
    with contextlib.redirect_stdout(external_file):
      print_commit_attr_to_screen(dict)
  external_file.close()

# parse arguments, there can be 2 - repo name and owner's name or 3 - + output filename

parser = argparse.ArgumentParser(
    prog='commitcheck',
    description='it will list last 30 commits for given repository')

parser.add_argument("-r", "--reponame", type=str, help="Repository Name")
parser.add_argument("-o", "--ownername", type=str, help="Owner Name")
parser.add_argument("-f", "--fileout", type=str, help="Output filename")
cliargs = parser.parse_args()

# Set headers and token - to be improved

load_dotenv()

token = os.getenv('GITHUB_API_TOKEN')
url = f"https://api.github.com/repos/{cliargs.ownername}/{cliargs.reponame}/commits"
output = requests.get(url,headers={'Authorization': f'token {token}'})

# If output file is specified dump stdout there, othwerwise print on screen

if cliargs.fileout:
  print_commit_attr_to_file(cliargs.fileout, output.json())
elif not (cliargs.fileout and output): 
  print_commit_attr_to_screen(output.json())
else:
  error_mesg = "Oops, no parameters, no data.."
  print(error_mesg)

# to do:
# - error handling, parsing parameters
# - parameter parser put into function
# - print_commit_attr_to_screen include return list (each line append to it) to reuse in other function