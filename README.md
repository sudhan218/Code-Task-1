CODE EXPLANATION


import os
import sys
import time
import hashlib
import shutil


In this part, the script starts by importing necessary Python modules. These modules are used for interacting with the operating system, working with time, calculating hash values, and performing file operations.

```
def calculate_md5(file_path):
    with open(file_path, "rb") as f:
        md5_hash = hashlib.md5()
        while chunk := f.read(8192):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()
```

This is a function named `calculate_md5` that calculates the MD5 hash of a given file. It reads the file in chunks and updates the hash value using the MD5 algorithm. The final hash value is returned as a hexadecimal string.

```
def log_event(log_file, message):
    with open(log_file, "a") as f:
        f.write(message + "\n")
```

The `log_event` function appends a given message to a log file. It opens the log file in append mode, writes the provided message along with a newline character to separate events, and then closes the file.

```
def synchronize_folders(source_folder, replica_folder, log_file):
    try:
        if not os.path.exists(replica_folder):
            os.makedirs(replica_folder)
```

The `synchronize_folders` function is the core of the synchronization process. It accepts three arguments: `source_folder` (path to the source directory), `replica_folder` (path to the replica directory), and `log_file` (path to the log file). Inside the `try` block, it checks if the replica folder exists and creates it if it doesn't.

```
        for root, _, files in os.walk(source_folder):
            relative_path = os.path.relpath(root, source_folder)
            replica_root = os.path.join(replica_folder, relative_path)

            if not os.path.exists(replica_root):
                os.makedirs(replica_root)
```

This loop iterates through the source folder using `os.walk`, which traverses directories and files recursively. For each directory (`root`), it calculates the relative path with respect to the source folder and constructs the corresponding directory structure in the replica folder.

```
            for file in files:
                source_file_path = os.path.join(root, file)
                replica_file_path = os.path.join(replica_root, file)

                if not os.path.exists(replica_file_path) or \
                   calculate_md5(source_file_path) != calculate_md5(replica_file_path):
                    shutil.copy2(source_file_path, replica_file_path)
                    log_event(log_file, f"Copied: {source_file_path} -> {replica_file_path}")
                    print(f"Copied: {source_file_path} -> {replica_file_path}")
```

Inside this nested loop, for each file in the `files` list of the current directory, it constructs the paths for both the source and replica files. It checks if the replica file doesn't exist or if the MD5 hashes of the source and replica files are different. If either condition is met, it copies the file using `shutil.copy2`, logs the event using `log_event`, and prints a message to indicate the copy operation.

```
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
```

This loop iterates through the replica folder in a similar fashion. For each file in the `files` list, it calculates the path in the source folder. If the source file doesn't exist, it removes the corresponding replica file, logs the event, and prints a message Which is about the removal.

```
    except Exception as e:
        log_event(log_file, f"An error occurred: {e}")
```

In case any exception occurs during the synchronization , this block catches the exception, logs an error message with the details to the log file, and handles the error perfectly.

```
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
```

The final part of the code checks if the script is being run directly (not imported as a module). If it's being run directly, it checks whether the correct number of command-line arguments (five in this case) have been provided. If not, it prints a usage message and exits with an error code.

If the arguments are provided correctly, the script assigns them to `source_folder`, `replica_folder`, `interval`, and `log_file` variables. Then, inside an infinite loop, it repeatedly calls the `synchronize_folders` function to synchronize the folders, waits for the specified interval using `time.sleep`, and repeats the process. Thus synchronization happens periodically based on the provided interval.


