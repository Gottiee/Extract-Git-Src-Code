#!/usr/bin/env python3

import argparse
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def argument():
    parser  = argparse.ArgumentParser(description="Extract git src code, extract /.git from a given URL and try to recompose the src code")
    parser.add_argument("-u", "--url", help="path/to/git/folder/.git", required=True)
    parser.add_argument('-b', '--blind', action='store_true', help="No directory listing")
    return parser.parse_args()

def add_git_path(url: str):
    path = Path(url)
    if path.parts[-1] != '.git':
        path = path / '.git'
    return str(path)

def dowload_git_folder(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(f"Error dowloading {url}: {e}")

def main():
    args = argument()
    url = add_git_path(args.url)
    if not args.blind:
        dowload_git_folder(url)

if __name__ == "__main__":
    main()