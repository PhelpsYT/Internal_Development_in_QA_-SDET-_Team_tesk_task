# Veeam Project
## Internal Development in QA (SDET) Team Task

This program performs one-way synchronization of two folders. Synchronization occurs periodically, with changes (file updates, copying, and removal operations) displayed in the console and logged to a file.

The system is designed using **hash tables**, allowing the verification of the integrity of the files by comparing the **SHA-256** hashes of the source with those of the replica efficiently.



### Requirements
- Python 3.4 or higher
- Libraries: `hashlib`, `os`, `time`, `shutil`, `argparse`, `logging`, `pathlib`

### Usage
```
python folder_sync.py [--source-folder SOURCE | -sf SOURCE] [--destination-folder REPLICA | -rf REPLICA] [--log-file-path LOG_FILE | -lf LOG_FILE] [--sync-interval TIME_INTERVAL | -i TIME_INTERVAL] [--sync-interval TIME_INTERVAL]
```
- `--source-folder` or `-sf`: Path to the source folder to be synchronized.
- `--destination-folder` or `-rf`: Path to the destination folder that will be updated to match the source folder.
- `--log-file-path` or `-lf`: Path to the log file.
- `--sync-interval` or `-i`: Time interval for synchronization in seconds (default: `60`).

## Example

To synchronize a folder named **source** to **replica** every **5 seconds**, with logs being saved in the file **logs**, run the following command:

```
python folder_sync.py -sf source -rf replica  -lf logs -i 5
```

The log file will appear as follows while the program is running:
![resim]()


## Notes

- The primary goal was to maintain clarity in the code while maximizing its efficiency. The development process took approximately 2 to 4 hours.
- If the source, replica, or log folders do not exist, the program will create them. It also supports full paths, allowing users to specify absolute paths in the initial configuration.
- The log file will automatically have a .log extension for proper log storage. It will contain all operations performed by the program, along with their execution timestamps. Additionally, all operations will be displayed in the console as specified in the requirements.
- The script continuously monitors the source folder and synchronizes it with the replica folder based on the user-specified time interval.
- Files in the replica will be updated if they exist but have differing hash values, created if they are not found in the replica folder, or deleted if they are present in the replica but absent from the source folder.
- The system is designed using hash tables for efficient file synchronization. In certain scenarios, implementing hash trees, such as Merkle trees, could offer additional efficiency. (To complex for a simple system)
- SHA-256 is used because it produces a longer hash (256 bits) that is more resistant to collisions and brute-force attacks. Unlike MD5 and SHA-1, which have known vulnerabilities, SHA-256 has no reported weaknesses.
- Special case: the program does not account for empty folders, as they do not store any information and do not generate a hash value for the hash table. A function to handle this is included but commented out between lines 58 and 68 of the code. Users can uncomment the line if they wish to synchronize empty folders, making both folders exactly the same all the time.
- To stop the script manually, use the keyboard interrupt (CTRL+C).




