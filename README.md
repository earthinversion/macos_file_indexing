# File Indexing and Searching on macOS
## 📌 Overview

This project provides a Python-based solution for indexing and searching files on a macOS system. The tool indexes all files in a specified volume, stores their metadata in an SQLite database, and allows fast searching using semantic similarity and fuzzy matching.

## 🚀 Features
- Index all files on a specified macOS volume
- Store metadata (file path, file kind, size, volume name, modified time) in SQLite
- Perform semantic search using FAISS and Sentence Transformers
- Fuzzy matching to find similar filenames
- Formatted search results in a human-readable table
- Fast and efficient due to FAISS caching

## 🔧 Installation

#### 1️⃣ Install Dependencies
```bash
pip install faiss-cpu sentence-transformers fuzzywuzzy pandas tabulate tqdm sqlite3 numpy python-Levenshtein
```

#### 2️⃣ Clone the Repository
```bash
git clone https://github.com/earthinversion/macos-file-indexing.git
cd macos-file-indexing
```

#### 3️⃣ Set Up the Database
- Edit the configuration in `confil.yaml` file
- Run the following command to build the indexing database
    ```bash
    python file_indexer.py
    ```

## 🔍 Searching for Files
- To search for a file, use:
    ```bash
    python search_files.py
    ```

## 🏆 Contributors
- Utpal Kumar - Developer & Maintainer
- Contributions are welcome! Feel free to open an issue or submit a PR.