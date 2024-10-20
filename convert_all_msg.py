import os
import sys

import outlookmsgfile as msg_to_eml

def convert(foldername: str):
    """Converts all .msg-files in foldername and in all subfolders.

    Args:
        foldername (path): A valid path in the filesystem.
    """
    msg_files = list()
    not_converted = list()
    
    for root, _, files in os.walk(foldername):
        for file in files:
            if file.endswith(".msg"):
                msg_files.append(os.path.join(root, file))
                
    for filename in msg_files:
        print("converting: " + filename + " ...", end="")
        conv_msg = msg_to_eml.load(filename)
        eml_filename = filename.removesuffix(".msg") + ".eml"
        if os.path.exists(eml_filename):
            print("\t!!! SKIPPING", end="")
            not_converted.append(filename)
        else:
            with open(eml_filename, "wb") as f:
                f.write(conv_msg.as_bytes())
        print()
        
    print("\n--- SUMMARY ---")
    print(f"Converted: {len(msg_files) - len(not_converted)} {"file" if len(msg_files) - len(not_converted) == 1 else "files"}.")
    if len(not_converted) > 0:
        print(f"The following {len(not_converted)} {"file" if len(not_converted) == 1 else "files"} were not converted:")
        print(not_converted)

def discover():
    pass

if __name__ == "__main__":
    if len(sys.argv) > 1 and (foldername := sys.argv[1]):
        if os.path.exists(foldername):
            foldername = sys.argv[1]
            convert(foldername)
        else:
            print("Not a valid foldername.")
    else:
        print("python3 convert_all_msg.py <base folder>")