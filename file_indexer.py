import os
import sqlite3
import time
import subprocess
from tqdm import tqdm  # Import tqdm for progress bar
import yaml

## Read the configuration file
with open("config.yaml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)

# Path to the SQLite database
DB_PATH = cfg['output_db_file']

# Directory to index ("/Volumes" for all mounted drives, or specify one)
ROOT_DIR = cfg['volume_to_index']

# Ensure the database file exists before connecting
def initialize_db():
    """Creates the database and the necessary table if not already present."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT UNIQUE,
            file_kind TEXT,
            size INTEGER,
            volume_name TEXT,
            modified_time REAL
        )
    """)
    conn.commit()
    conn.close()

def get_volume_name(file_path):
    """Extracts the actual volume name from the file path."""
    parts = file_path.split(os.sep)  # Split the path by '/'
    if len(parts) > 2 and parts[1] == "Volumes":
        return parts[2]  
    return "Macintosh HD"  # Default to internal drive if not under /Volumes

def get_file_kind(file_path):
    """Determines the file kind using the `file` command."""
    try:
        result = subprocess.run(["file", "--brief", file_path], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception:
        return "Unknown"

def estimate_total_files(root_directory):
    """Estimates the total number of files for progress bar initialization."""
    total_files = 0
    for _, _, filenames in os.walk(root_directory):
        total_files += len(filenames)
    return total_files

def index_files(root_directory):
    """Scans the given directory and updates the database with a progress bar."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    new_files = set()
    total_files = estimate_total_files(root_directory)  # Estimate total files for tqdm

    with tqdm(total=total_files, desc="Indexing Files", unit="file") as pbar:
        for dirpath, _, filenames in os.walk(root_directory):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                try:
                    file_stat = os.stat(file_path)
                    file_size = file_stat.st_size
                    file_kind = get_file_kind(file_path)
                    volume_name = get_volume_name(file_path)
                    new_files.add(file_path)

                    cursor.execute("""
                        INSERT INTO files (path, file_kind, size, volume_name, modified_time)
                        VALUES (?, ?, ?, ?, ?)
                        ON CONFLICT(path) DO UPDATE SET
                            file_kind=excluded.file_kind,
                            size=excluded.size,
                            volume_name=excluded.volume_name,
                            modified_time=excluded.modified_time
                    """, (file_path, file_kind, file_size, volume_name, file_stat.st_mtime))

                    pbar.update(1)  # Update progress bar

                except FileNotFoundError:
                    continue  # File might have been removed before processing

    # Remove entries for missing files
    cursor.execute("SELECT path FROM files")
    stored_files = {row[0] for row in cursor.fetchall()}

    deleted_files = stored_files - new_files
    if deleted_files:
        cursor.executemany("DELETE FROM files WHERE path = ?", [(file,) for file in deleted_files])
        print(f"Removed {len(deleted_files)} missing files from the database.")

    conn.commit()
    conn.close()
    print(f"Indexing complete. Indexed {len(new_files)} files, removed {len(deleted_files)} files.")

def main():
    start_time = time.time()
    initialize_db()
    index_files(ROOT_DIR)
    print(f"Finished in {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
