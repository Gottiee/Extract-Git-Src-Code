# Extract-Git-Src-Code

Extract Git Source code is a tool which download the .git folder of a given URL and recompose the source code.

:warning: Directory listing should be activated

```bash
usage: extract_git_src_code.py [-h] -u URL [-o OUTPUT] [-v] [--onlyDownload] [--onlyExtract]

Extract git src code, extract /.git from a given URL and try to recompose the src code

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     https://url.net/path/to/git/folder/.git
  -o OUTPUT, --output OUTPUT
                        Name of extract .git folder (default='git')
  -v, --verbose         Print additional informations
  --onlyDownload        Do not extract source code, only '.git' directory
  --onlyExtract         Do not download '.git' directory and assume it already exist to perform the soure code extraction
```