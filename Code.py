import os
import sys
import time
import hashlib
import shutil

# Calculate MD5 hash of a file
def calculate_md5(file_path):
    with open(file_path, "rb") as f:
        md5_hash = hashlib.md5()
        while chunk := f.read(8192):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

# Log an event to the specified log file
def log_event(log_file, message):
    with open(log_file, "a") as f:
        f.write(message + "\n")

# Synchronize the source and replica folders
def synchronize_folders(source_folder, replica_folder, log_file):
    try:
        # Ensure replica folder exists
        if not os.path.exists(replica_folder):
            os.makedirs(replica_folder)

        # Copy new or modified files from source to replica
        for root, _, files in os.walk(source_folder):
            relative_path = os.path.relpath(root, source_folder)
            replica_root = os.path.join(replica_folder, relative_path)

            if not os.path.exists(replica_root):
                os.makedirs(replica_root)

            for file in files:
                source_file_path = os.path.join(root, file)
                replica_file_path = os.path.join(replica_root, file)

                # Copy if file is missing in replica or content differs
                if not os.path.exists(replica_file_path) or \
                   calculate_md5(source_file_path) != calculate_md5(replica_file_path):
                    shutil.copy2(source_file_path, replica_file_path)
                    log_event(log_file, f"Copied: {source_file_path} -> {replica_file_path}")
                    print(f"Copied: {source_file_path} -> {replica_file_path}")

        # Remove files from replica that are not in source
        for root, _, files in os.walk(replica_folder):
            relative_path = os.path.relpath(root, replica_folder)
            source_root = os.path.join(source_folder, relative_path)

            for file in files:
                source_file_path = os.path.join(source_root, file)
                replica_file_path = os.path.join(root, file)

                if not os.path.exists(source_file_path):
                    os.remove(replica_file_path)
                    log_event(log_file, f"Removed: {replica_file_path}")
                    print(f"Removed: {replica_file_path}")

    except Exception as e:
        log_event(log_file, f"An error occurred: {e}")

# Main script execution
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python sudhan.py source_folder replica_folder interval_in_seconds log_file_path")
        sys.exit(1)

    source_folder = sys.argv[1]
    replica_folder = sys.argv[2]
    interval = int(sys.argv[3])
    log_file = sys.argv[4]

    while True:
        synchronize_folders(source_folder, replica_folder, log_file)
        time.sleep(interval)

