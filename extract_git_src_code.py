#!/usr/bin/env python3

import argparse, os, requests, git, shutil
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse, urljoin
from pathlib import Path

def print_v(str, verbose):
    if verbose:
        print(str)

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
    parser.add_argument("-u", "--url", help="https://url.net/path/to/git/folder/.git", required=True)
    parser.add_argument('-o', '--output', help='Name of extract .git folder (default=\'git\')', default='git')
    parser.add_argument('-v', '--verbose', help='Print additional informations', action='store_true', default=False)
    parser.add_argument('--onlyDownload',action='store_true', help="Do not extract source code, only '.git' directory", default=False)
    parser.add_argument('--onlyExtract',action='store_true', help="Do not download '.git' directory and assume it already exist to perform the soure code extraction", default=False)
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
        print(f"Error dowloading {url}")

def dowload_git_folder(url:str, path: Path, verbose):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True) 
        for link in links:
            dir = link['href']
            if dir == "../" or dir == "/" or dir.startswith("?") or link.string.lower() == "parent directory":
                continue
            
            if dir.endswith('/'): 
                new_url = url + dir
                dir = dir[:-1]
                new_path = path / dir
                create_directory(str(new_path))
                dowload_git_folder(new_url, new_path, verbose)
            else:
                file_path = path / dir
                print_v(f"\tDowloading: {str(file_path)}", verbose)
                create_file(str(file_path), dowload_file(url + dir))
    except requests.exceptions.RequestException as e:
        print(f"Error dowloading {url}: {e}")

def open_read(path: str):
    try:
        with open(str(path), 'r') as file:
            return file.read()
    except Exception as e:
        print(f"File error at {str(path)} : {e}")
        return None

def get_src_code(path: Path, verbose, base: Path):
    head_path = path / "HEAD"
    content = open_read(str(head_path))
    if content == None:
        print(f"End of the program")
        return
    if content.endswith("\n"):
        content = content[:-1]
    if content.startswith("ref: "):
        head = content.split("ref: ", 1)[1]
        new_path = path / head
        git_head = open_read(str(new_path))
        if git_head == None:
            print(f"End of the program")
            return
        if git_head.endswith("\n"):
            git_head = git_head[:-1]
    else:
        git_head = content
    print_v(f"\tGit HEAD: {git_head}", verbose)
    repo = git.Repo(str(path))
    repo.git.archive("--format", "zip", "--output", "source.zip", git_head)
    extract_path = base / "src_code"
    base = base / "source.zip"
    shutil.unpack_archive(str(base), str(extract_path))
    print_v(f"\tSource code extracted at {str(extract_path)}", verbose)
    os.system(f"rm -f {str(base)}")

def main():
    args = argument()
    base = Path(args.output)
    path = base / ".git"
    if not args.onlyExtract:
        print(f"Downloading...")
        url = add_git_path(args.url)
        create_directory(args.output)
        create_directory(str(path))
        dowload_git_folder(url, path, args.verbose)
        print(f"Download done\n")
    if not args.onlyDownload:
        print(f"Extract source code...")
        get_src_code(path, args.verbose, base)
        src = base / "src_code"
        print(f"Source code extracted")

if __name__ == "__main__":
    main()