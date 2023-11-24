#!/usr/bin/env python3

import argparse, os, requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse, urlunparse
from pathlib import Path

def create_directory(directory_path):
    try:
        os.makedirs(directory_path)
        if os.path.exists(directory_path) and os.path.isdir(directory_path):
            pass
            # print(f"Directory '{directory_path}' created successfully.")
        else:
            raise OSError(f"Failed to create directory '{directory_path}'.")
    except OSError as e:
        print(f"Error creating directory '{directory_path}': {e}")

def create_file(file_path, content=None):
    try:
        with open(file_path, 'w') as file:
            if content is not None:
                file.write(content)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            pass
            # print(f"File '{file_path}' created successfully.")
        else:
            raise OSError(f"Failed to create file '{file_path}'.")
    except OSError as e:
        print(f"Error creating file '{file_path}': {e}")

def argument():
    parser  = argparse.ArgumentParser(description="Extract git src code, extract /.git from a given URL and try to recompose the src code")
    parser.add_argument("-u", "--url", help="path/to/git/folder/.git", required=True)
    parser.add_argument('-b', '--blind', action='store_true', help="No directory listing")
    parser.add_argument('-o', '--output', help='Name of extract .git folder (default=\'git\')', default='git')
    return parser.parse_args()

def add_git_path(url: str):
    if url[-1] == '/':
       url = url[:-1] 
    parsed_url = urlparse(url)
    if not parsed_url.path.endswith(".git"):
        new_path = parsed_url.path + "/.git"
        modified_url = urlunparse(parsed_url._replace(path=new_path))
        return modified_url
    return url

def dowload_git_folder(url:str, depth=1):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True) 
        for link in links:
            if link['href'].endswith('/') : 
                create_directory

    except requests.exceptions.RequestException as e:
        print(f"Error dowloading {url}: {e}")

def main():
    args = argument()
    url = add_git_path(args.url)
    create_directory(args.output)
    base = Path(args.output)
    create_directory(str(base / ".git"))
    if not args.blind:
        dowload_git_folder(url)

if __name__ == "__main__":
    main()