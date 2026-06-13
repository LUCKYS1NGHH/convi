#!/usr/bin/env python3
import os, sys, subprocess
from PIL import Image
import platform
import ctypes

PURPLE_TEXT = "\33[95m"
RESET = "\33[0m"

def get_timestamps(file):
    return os.path.getctime(file), os.path.getmtime(file)

def set_timestamps(target, created, modified):
    if platform.system() == "Windows":
        FILETIME = ctypes.c_ulonglong
        handle = ctypes.windll.kernel32.CreateFileW(target, 256, 0, None, 3, 128, None)
        if handle != -1:
            ctypes.windll.kernel32.SetFileTime(handle, ctypes.byref(FILETIME(int(created * 1e7) + 116444736000000000)), None, None)
            ctypes.windll.kernel32.CloseHandle(handle)
    os.utime(target, (modified, modified))

def conversion(image_path, Format, copy_timestamps=False):
    print("Converting...")
    print("-"*20)
    img = Image.open(image_path)
    original_image = os.path.splitext(image_path)[0]
    converted_image = original_image + f".{Format}"
    img.save(converted_image, Format)
    converted_size = os.path.getsize(converted_image)
    original_size = os.path.getsize(image_path)
    print(f"Image Converted!\n{converted_image}")
    print(f"Original Size: {original_size/1024:.2f}KB")
    print(f"Converted Size: {converted_size/1024:.2f}KB")
    if copy_timestamps:
        print("Timestamps Copied!")
        set_timestamps(converted_image, *get_timestamps(image_path))

def inter_mode():
    print(
    "\n[1] Batch Image Compression",
    "\n[2] Single Image Compression",
    )
    choice = input("\nChoose (1/2): ")

    if choice == "1":
        images_in_folder = input("Enter the image directory for conversion: ")
        flag = input("Enter the flag: ").lower()
        image_name = flag
        if os.path.exists(images_in_folder):
            imgs = os.listdir(images_in_folder)
            for img in imgs:
                print(PURPLE_TEXT,img,RESET)
            if img.endswith((".jpg", ".png", ".jpeg", ".webp")):
                    convert_to = None
                    if "--jpeg" in flag or "--jpg" in flag:
                        convert_to = "jpeg"
                    elif "--png" in flag:
                        convert_to = "png"
                    elif "--webp" in flag:
                        convert_to = "webp"
                    elif "--ico" in flag:
                        convert_to = "ico"
                    else:
                        print("No valid format flag found!")
                        sys.exit(1)

                    for img_file in os.listdir(images_in_folder):
                        if img_file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                            full_path = os.path.join(images_in_folder, img_file)
                            conversion(full_path, convert_to, copy_timestamps="-t" in flag)
    else:
        image_name = input("Enter Image Name and Flags: ").strip().split() # -jpeg, -png, -webp flags for image conversion and -t for copying timestamps
        raw_input = image_name
        image_name = image_name[0]
        if "--jpeg" in raw_input or "--jpg" in raw_input:
            JPG = "jpeg"
            conversion(image_name, Format=JPG, copy_timestamps="-t" in raw_input)
        elif "--png" in raw_input:
            if ".png" in raw_input and "--jpeg" in raw_input:
                print("You can't convert png to jpeg, you can try -webp instead.")
                sys.exit(1)
            PNG = "png"
            conversion(image_name, Format=PNG, copy_timestamps="-t" in raw_input)
        elif "--webp" in raw_input:
            WEBP = "webp"
            conversion(image_name, Format=WEBP, copy_timestamps="-t" in raw_input)
        elif "--ico" in  raw_input:
            ICO = "ico"
            conversion(image_name, Format=ICO, copy_timestamps="-t" in raw_input)
        else:
            print("IT SUCKED!")

def get_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-P", "--path", required=True, help="Image path")
    parser.add_argument("-w", "--webp", action="store_true", help="Webp image format")
    parser.add_argument("-p", "--png", action="store_true", help="Png image format")
    parser.add_argument("-j", "--jpg", action="store_true", help="Jpeg image format")
    parser.add_argument("-t", "--timestamps", action="store_true", help="Inherit the file timestamps (only modified) from original to converted image.")
    parser.add_argument("-l", "--lastimg", action="store_true", help="Auto greps the recent image of given directory.")
    return parser.parse_args()

def cli_mode():
    args = get_args()
    if any(flag in sys.argv for flag in ("-w", "--webp", "-p", "--png", "-j", "--jpg")):
        path = args.path

        if not os.path.exists(path):
            print("Path doesn't exists.")
            sys.exit(1)

        if args.lastimg:
            if not os.path.isdir(args.path):
                print("Directory need for the recent image.")
                sys.exit(1)

            cmd = (
            'find "$(pwd)" -maxdepth 1 -type f '
            '\\( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.webp" \\) '
            '-printf "%T@ %p\\n" | sort -rn | head -1 | cut -d" " -f2-'
            )

            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=args.path)
            path = result.stdout.strip() # latest file
            print(f"Grepped the recent image {path}")

        if not os.path.isfile(path):
            print("It's a directory.")
            sys.exit(1)

        if args.webp:
            conversion(path, "webp", copy_timestamps=args.timestamps)
        elif args.png:
            conversion(path, "png", copy_timestamps=args.timestamps)
        elif args.jpg:
            conversion(path, "jpeg", copy_timestamps=args.timestamps)
    else:
        print("No valid format flag found!")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cli_mode()
    else:
        inter_mode()
