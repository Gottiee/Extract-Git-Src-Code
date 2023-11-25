#!/usr/bin/env python3

import argparse, os, requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse, urljoin
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
        with open(file_path, 'wb') as file:
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
        return modified_url + "/"
    return url + "/"

def dowload_file(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Error dowloading {url}: {e}")

def dowload_git_folder(url:str, path: Path, depth=1):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True) 
        for link in links:
            dir = link['href']
            if dir == "../":
                continue
            if dir.endswith('/'): 
                new_url = url + dir
                dir = dir[:-1]
                new_path = path / dir
                create_directory(str(new_path))
                dowload_git_folder(new_url, new_path)
            else:
                file_path = path / dir
                print(f"Dowloading: {str(file_path)}")
                create_file(str(file_path), dowload_file(url + dir))

    except requests.exceptions.RequestException as e:
        print(f"Error dowloading {url}: {e}")

def main():
    args = argument()
    url = add_git_path(args.url)
    create_directory(args.output)
    base = Path(args.output)
    path = base / ".git"
    create_directory(str(path))
    if not args.blind:
        dowload_git_folder(url, path)

if __name__ == "__main__":
    main()