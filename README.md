# Toolbelt

A very useful command-line multi-tool for common terminal tasks.

## Features

- Generate secure passwords
- Hash text or files
- Validate and pretty-print JSON
- Find duplicate files in a directory tree

## Usage

```bash
python3 toolbelt.py pwgen 24
python3 toolbelt.py hash --text "hello"
python3 toolbelt.py hash --file ./some.bin --algo sha512
cat data.json | python3 toolbelt.py jsonfmt --sort-keys
python3 toolbelt.py dupes .
```
