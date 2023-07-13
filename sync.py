import sys
import os
import filecmp
import shutil
import argparse

def sync_folders(source_folder, target_folder):
    dcmp = filecmp.dircmp(source_folder, target_folder)
    
    # Copy files from the source folder to the target folder
    for name in dcmp.left_only:
        source_path = os.path.join(source_folder, name)
        target_path = os.path.join(target_folder, name)
        if os.path.isfile(source_path):
            shutil.copy2(source_path, target_path)
        else:
            shutil.copytree(source_path, target_path)
        print(f"Copying: {source_path} -> {target_path}")
    
    # Remove files that are missing in the source folder
    for name in dcmp.right_only:
        target_path = os.path.join(target_folder, name)
        if os.path.isfile(target_path):
            os.remove(target_path)
            print(f"Removing: {target_path}")
        else:
            shutil.rmtree(target_path)
            print(f"Removing: {target_path}")
    
    # Recursively synchronize subfolders
    for sub_dcmp in dcmp.subdirs.values():
        sync_folders(
            os.path.join(source_folder, sub_dcmp.dirname),
            os.path.join(target_folder, sub_dcmp.dirname)
        )

# Create the argument parser
parser = argparse.ArgumentParser(description="Script to synchronize two folders.")
parser.add_argument("-s", "--source", type=str, help="Path to the source folder.")
parser.add_argument("-d", "--destination", type=str, help="Path to the target folder.")

# Parse the command-line arguments
args = parser.parse_args()

# Check for required arguments
if not args.source or not args.destination:
    parser.print_help()
else:
    source_folder = args.source
    target_folder = args.destination
    
    # Check if the target folder exists and create it if it doesn't
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
        print(f"Created target folder: {target_folder}")
    
    sync_folders(source_folder, target_folder)
