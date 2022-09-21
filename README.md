# dcm2png

## Prerequisite

### Python
* Python 3.10.7

## How to install
```
$ pip install -r requirements.txt
```

## How to use
```
python dcm2png.py --help

usage: dcm2png.py [-h] --dcm-dir DCM_DIR --png-dir PNG_DIR [--stem-suffix STEM_SUFFIX]

options:
  -h, --help            show this help message and exit
  --dcm-dir DCM_DIR     a path to a directory to search for dcm files recursively
  --png-dir PNG_DIR     a path to a directory to output png files
  --stem-suffix STEM_SUFFIX
                        a suffix of filename added to output png files
```
