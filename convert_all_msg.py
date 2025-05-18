import os
import sys

import outlookmsgfile as msg_to_eml

"""
Add in compoundfiles.streams.CompoundFileMiniStream.close():
    except Exception as e:
      pass  # Suppress Exception: if file can not be close, it's presumably already closed.
There must be some error in outlookmsgfile, but I can seem to find it..
"""

def convert(foldername: str):
    """Converts all .msg-files in foldername and in all subfolders.

    Args:
        foldername (path): A valid path in the filesystem.
    """
    msg_files = list()
    not_converted = list()
    
    # Search the given directory for .msg-files.
    for root, _, files in os.walk(foldername):
        for file in files:
            if file.endswith(".msg"):
                msg_files.append(os.path.join(root, file))

    # Convert all found files.
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
            print("\t Done", end="")
        print()
        
    print("\n--- SUMMARY ---")
    print(f"Converted: {len(msg_files) - len(not_converted)} {"file" if len(msg_files) - len(not_converted) == 1 else "files"}.")
    if len(not_converted) > 0:
        print(f"The following {len(not_converted)} {"file" if len(not_converted) == 1 else "files"} were not converted:")
        for nc in not_converted:
            print(nc)

if __name__ == "__main__":
    if len(sys.argv) > 1 and (foldername := sys.argv[1]):
        if os.path.exists(foldername):
            convert(foldername)
        else:
            print("Not a valid foldername.")
    else:
        print("python3 convert_all_msg.py <base folder>")