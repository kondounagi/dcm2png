# dcm2png

## Prerequisite

### Python

- Python 3.10.7

## How to install

```bash
$ pip install -r requirements.txt
```

## How to use

```bash
$ python dcm2png.py --help

 Usage: dcm2png.py [OPTIONS] DCM_DIR PNG_DIR

╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    dcm_dir      PATH  a path to a directory to search for dcm files recursively [default: None] [required] │
│ *    png_dir      PATH  a path to a directory to output png files [default: None] [required]                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --verbose               --no-verbose             whether to show verbose messages [default: no-verbose]      │
│ --stem-suffix                           TEXT     a suffix of filename added to output png files              │
│                                                  [default: out]                                              │
│ --max-workers                           INTEGER  the maximum number of workers to convert dcm files to png   │
│                                                  files                                                       │
│                                                  [default: 64]                                               │
│ --install-completion                             Install completion for the current shell.                   │
│ --show-completion                                Show completion for the current shell, to copy it or        │
│                                                  customize the installation.                                 │
│ --help                                           Show this message and exit.                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
