# Convi

A simple CLI tool for converting images format to Jpeg/Png/Webp in GNU/Linux.

## Usage

```
$ convi -h

options:
  -h, --help            show this help message and exit
  -P, --path PATH [PATH ...]
                        Image path
  -w, --webp            Webp image format
  -p, --png             Png image format
  -j, --jpg             Jpeg image format
  -t, --timestamps      Inherit the file timestamps (only modified and accessed) from original to converted image.
  -l, --lastimg         Auto greps the recent image (by modification date) of given directory.
  -v, --verbose         Enable verbose output
  -L, --lossless        Lossless webp images (quality 100)
  -c, --compress COMPRESS
                        Compress the image by number (defualt 90)
  -s, --size SIZE       Max pixel size to resize (preserves aspect ratio)
```

## Dependencies

Requires Python 3 and pillow library.

> Python might be already installed in your system

```bash
pip install pillow # or install `python-pillow` as system-wide through your package manager
```

## Install

```bash
git clone --depth=1 https://github.com/LUCKYS1NGHH/convi.git
sudo cp convi/convi.py /usr/local/bin/convi
sudo chmod 755 /usr/local/bin/convi
```

## Author

LUCKYS1NGHH / https://github.com/LUCKYS1NGHH
