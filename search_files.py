import sqlite3
import faiss
import numpy as np
import os
import pickle
import pandas as pd
from tabulate import tabulate
from sentence_transformers import SentenceTransformer
from fuzzywuzzy import process
from datetime import datetime
import yaml

# Load the SentenceTransformer model for text embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")


## Read the configuration file
with open("config.yaml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)


# Database Path
DB_PATH = cfg['output_db_file']
CACHE_FILE = "file_embeddings.pkl"  # For caching FAISS index

def ask_to_search_again():
    """Asks the user if they want to search again and deletes the cache file if they do."""

    if os.path.exists(CACHE_FILE):
        response = input("Do you want to rebuild the search cache? (yes/no): ").strip().lower()
        if response == "yes":
            os.remove(CACHE_FILE)
            print("Cache file deleted.")
            return True
        elif response == "no":
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


def load_file_data():
    """Loads all file data (path, kind, size, volume, modified time) from the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT path, file_kind, size, volume_name, modified_time FROM files")
    file_data = cursor.fetchall()
    conn.close()

    # Extract filenames from full paths
    file_names = [os.path.basename(row[0]) for row in file_data]
    return file_data, file_names

def build_faiss_index(file_names):
    """Builds and caches a FAISS index for fast filename similarity search."""
    if not file_names:
        return None

    try:
        # Load cached FAISS index if available
        with open(CACHE_FILE, "rb") as f:
            index, stored_file_names = pickle.load(f)
        return index, stored_file_names
    except (FileNotFoundError, EOFError, pickle.UnpicklingError):
        pass  # If loading fails, proceed with rebuilding

    print("🔄 Generating FAISS index (this might take a few seconds)...")
    
    # Generate embeddings for all filenames
    file_vectors = np.array(model.encode(file_names), dtype=np.float32)

    # Use HNSW index for faster searching
    index = faiss.IndexHNSWFlat(file_vectors.shape[1], 32)
    index.add(file_vectors)

    # Cache index for future use
    with open(CACHE_FILE, "wb") as f:
        pickle.dump((index, file_names), f)

    print("✅ FAISS index built and cached.")
    return index, file_names  # Ensure variables are assigned

def search_files(query):
    """Searches for a file using FAISS similarity and fuzzy matching, then displays results in a table."""
    file_data, file_names = load_file_data()

    if not file_names:
        print("No files found in the database.")
        return

    index, stored_file_names = build_faiss_index(file_names)
    if index is None:
        print("FAISS index could not be created.")
        return

    # Exact match check (compare only filenames, not full paths)
    if query in stored_file_names:
        exact_index = stored_file_names.index(query)
        found_file = file_data[exact_index]
        print("\n✅ Exact match found:")
        display_results([found_file])  # Display in tabular format
        return

    # Encode query into vector space
    query_vector = np.array(model.encode([query]), dtype=np.float32)

    # Perform FAISS search
    _, closest_indices = index.search(query_vector, k=5)
    closest_files = [file_data[idx] for idx in closest_indices[0]]

    print("\n❌ Exact match not found. Suggested files:")
    display_results(closest_files)

    # Additional fuzzy matching (Levenshtein distance)
    best_match = process.extractOne(query, stored_file_names)
    if best_match:
        best_match_index = stored_file_names.index(best_match[0])
        print("\n🔍 Best fuzzy match:")
        display_results([file_data[best_match_index]])

def format_size(size_bytes):
    """Converts file size from bytes to human-readable format (KB, MB, GB, etc.)."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024**2:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024**3:
        return f"{size_bytes / 1024**2:.2f} MB"
    else:
        return f"{size_bytes / 1024**3:.2f} GB"

def format_time(timestamp):
    """Converts Unix timestamp to human-readable format."""
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

def display_results(files):
    """Displays file search results in a formatted table with human-readable size & time."""
    df = pd.DataFrame(files, columns=["Path", "File Kind", "Size (bytes)", "Volume", "Modified Time"])

    # Apply human-readable formats
    df["Size (bytes)"] = df["Size (bytes)"].apply(format_size)
    df["Modified Time"] = df["Modified Time"].apply(format_time)

    print(tabulate(df, headers="keys", tablefmt="pretty"))

if __name__ == "__main__":
    
    ask_to_search_again()

    while True:
        query = input("Enter filename to search: ")
        if not query:
            break
        search_files(query)
