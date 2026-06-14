# Convi

A simple CLI tool for converting image formats to JPEG/PNG/WEBP for GNU/Linux.

## Usage

```
$ convi -h
usage: conv [-h] -P PATH [-w] [-p] [-j] [-t] [-l] [-v]

options:
  -h, --help        show this help message and exit
  -P, --path PATH   Image path
  -w, --webp        Webp image format
  -p, --png         Png image format
  -j, --jpg         Jpeg image format
  -t, --timestamps  Inherit the file timestamps (only modified and accessed) from original to converted image
  -l, --lastimg     Auto greps the recent image (by modification date) of given directory
  -v, --verbose     Enable verbose output
```

## Install

```bash
git clone --depth=1 https://github.com/LUCKYS1NGHH/convi.git
sudo cp convi/convi.py /usr/local/bin/convi # for only your user account, replace /usr/local/bin with $HOME/.local/bin
```

## Dependencies

Requires Python 3 and pillow library.

```
pip install pillow # or install `python-pillow` as system-wide through your package manager
```

## Author

LUCKYS1NGHH / https://github.com/LUCKYS1NGHH

