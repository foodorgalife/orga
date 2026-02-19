# Toolbelt

A very useful command-line multi-tool for common terminal tasks.

## Where you can use this tool

You can use `toolbelt.py` anywhere you can run Python 3:

- **Your local machine** (macOS, Linux, Windows with Python installed)
- **Remote servers** over SSH for quick ops/debugging tasks
- **Dev containers / CI jobs** for lightweight scripting steps
- **Project repositories** as a utility script for developers

Typical situations where it helps:

- Need a strong password quickly (`pwgen`)
- Need to verify file or string integrity (`hash`)
- Need to validate or reformat JSON (`jsonfmt`)
- Need to clean up duplicate files in folders (`dupes`)

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

## Getting help

```bash
python3 toolbelt.py --help
python3 toolbelt.py hash --help
```
