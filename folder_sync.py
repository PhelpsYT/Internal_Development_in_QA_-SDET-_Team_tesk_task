import time
import shutil
import hashlib
import logging
import argparse
from pathlib import Path

# Parse command-line arguments and return them.
def parse_arguments():
    parser = argparse.ArgumentParser(prog='folder_sync', description='Synchronizes two folders')
    parser.add_argument('-sf', '--source_folder', type=str, default='source_folder', help='Source folder path')
    parser.add_argument('-rf', '--replica_folder', type=str, default='replica_folder', help='Replica folder path')
    parser.add_argument('-lf', '--log_file', type=str, default='log_file', help='Log file path')
    parser.add_argument('-i', '--interval', type=int, default=10, help='Synchronization interval in seconds')
    return parser.parse_args()

# Create source and replica directories if they do not exist and set up logging.
def setup_directories(arguments):    
    Path(arguments.source_folder).mkdir(parents=True, exist_ok=True)
    Path(arguments.replica_folder).mkdir(parents=True, exist_ok=True)
    Path(arguments.log_file).parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(filename=Path(arguments.log_file).with_suffix('.log'), encoding='utf-8', level=logging.INFO,    format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.info(f"Start Config: [Source folder: {arguments.source_folder}, Replica folder: {arguments.replica_folder}, Log file: {arguments.log_file}.log, Synchronization interval: {arguments.interval} seconds]")
    
# Generate a hash table given folder path with their SHA-256 hashes.
def generate_hash_table(folder_path):
    return {file_path: hashlib.sha256(file_path.read_bytes()).hexdigest()
            for file_path in folder_path.rglob('*') if file_path.is_file()}

# Synchronize files between the source and replica folders based on their respective hashe table.
def synchronize_folders(source_folder, replica_folder):
    source_folder = Path(source_folder)
    replica_folder = Path(replica_folder)
    
    # Create hash tables for both source and replica
    source_hash_table = generate_hash_table(source_folder)
    replica_hash_table = generate_hash_table(replica_folder)

    # Synchronize files (create/update)
    for source_path, source_hash in source_hash_table.items():
        replica_path = replica_folder / source_path.relative_to(source_folder)
        replica_hash = replica_hash_table.get(replica_path)

        if replica_hash != source_hash:  # Update if hashes are different or create if the file doesn't exist
            logging.info(f"{'Updating' if replica_hash != None else 'Creating'} file: {replica_path}")
            replica_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, replica_path)

    # Delete files in replica that are not in source
    for replica_path in replica_hash_table:
        source_path = source_folder / replica_path.relative_to(replica_folder)
        if not source_path.exists():
            logging.info(f"Deleting file: {replica_path}")
            replica_path.unlink()

    # Special case: Takes care of empty folders since they dont have hash values but still exist ## Uncomment if empty folders matter
    """
    for folder in Path(source_folder).rglob('*'):
        if folder.is_dir():
            if not any(folder.iterdir()):
                (replica_folder / folder.relative_to(source_folder)).mkdir(parents=True, exist_ok=True)

            replica_folder_path = replica_folder / folder.relative_to(source_folder)
            if not replica_folder_path.exists() and not any(replica_folder_path.iterdir()):
                replica_folder_path.rmdir()
    """
    
# Starting point of the program
if __name__ == '__main__':
    arguments = parse_arguments()
    setup_directories(arguments)

    while True:
        synchronize_folders(arguments.source_folder, arguments.replica_folder)
        time.sleep(arguments.interval)