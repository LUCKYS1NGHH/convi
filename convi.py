#!/usr/bin/env python3
import os, sys, subprocess
from PIL import Image

BLUE = "\33[34m"
PURPLE = "\33[35m"
RESET = "\33[0m"

def get_timestamps(file):
    # get modified and accessed time
    return os.path.getmtime(file), os.path.getctime(file)

def set_timestamps(target, modified, access):
    # set modified and accessed time
    os.utime(target, (modified, access))

def conversion(image_path, Format, copy_timestamps=False, verbose=True):
    """Convert the image to given format and show the result if verbose"""
    img = Image.open(image_path)

    # add given format in the converted image filename
    original_image = os.path.splitext(image_path)[0]
    converted_image = original_image + f".{Format}"

    img.save(converted_image, Format)

    if verbose:
        print(f"\n{PURPLE}{converted_image}{RESET}")
        print(f"Original  : {os.path.getsize(image_path)/1024:.2f}KB")
        print(f"Converted : {os.path.getsize(converted_image)/1024:.2f}KB")
    if copy_timestamps:
        if verbose:
            print(f"{BLUE}Timestamps Inherited{RESET}")
        set_timestamps(converted_image, *get_timestamps(image_path))

def get_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-P", "--path", required=True, nargs="+", help="Image path")
    parser.add_argument("-w", "--webp", action="store_true", help="Webp image format")
    parser.add_argument("-p", "--png", action="store_true", help="Png image format")
    parser.add_argument("-j", "--jpg", action="store_true", help="Jpeg image format")
    parser.add_argument("-t", "--timestamps", action="store_true", help="Inherit the file timestamps (only modified and accessed) from original to converted image.")
    parser.add_argument("-l", "--lastimg", action="store_true", help="Auto greps the recent image (by modification date) of given directory.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()

def main():
    args = get_args()
    if any(flag in sys.argv for flag in ("-w", "--webp", "-p", "--png", "-j", "--jpg")):

        files = args.path

        # iterate multiple files (for *, ?, [] etc.)
        for path in files:
            if not os.path.exists(path):
                print("Path doesn't exists.")
                sys.exit(2)

            if args.lastimg:
                if not os.path.isdir(path):
                    print("Directory need for the recent image.")
                    sys.exit(20)

                # command for getting the last image filename by modtime from the directory (YES, looks ugly but works)
                cmd = (
                'find "$(pwd)" -maxdepth 1 -type f '
                '\\( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.webp" \\) '
                '-printf "%T@ %p\\n" | sort -rn | head -1 | cut -d" " -f2-'
                )

                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=path)
                path = result.stdout.strip() # latest file
                print(f"\n{BLUE}Grepped the recent image{RESET} {path}")

            if not os.path.isfile(path):
                print("It's a directory.")
                sys.exit(21)

            # image format according flag argument
            if args.webp:
                target_format = "webp"
            elif args.png:
                target_format = "png"
            elif args.jpg:
                target_format = "jpeg"

            conversion(path, target_format, copy_timestamps=args.timestamps, verbose=args.verbose)
    else:
        print("No valid format flag found.")
        sys.exit(64)

if __name__ == "__main__":
    main()

# A simple CLI tool for converting image file formats
# By LUCKYS1NGHH (or LUCKY)
# Official Repository URL: https://github.com/LUCKYS1NGHH/convi
# LICENSE: GPLv3

