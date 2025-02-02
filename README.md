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
    python search_files.py                                                                                                                 ok  index_files py 
    Do you want to rebuild the search cache? (yes/no): no
    Enter filename to search: location_info.yaml

    ❌ Exact match not found. Suggested files:
    +---+-------------------------------------------------------------------+------------------------------------+--------------+-----------+---------------------+
    |   |                               Path                                |             File Kind              | Size (bytes) |  Volume   |    Modified Time    |
    +---+-------------------------------------------------------------------+------------------------------------+--------------+-----------+---------------------+
    | 0 | /Volumes/QSIS_DISK/event_data_download_waveform_api/._config.yaml | AppleDouble encoded Macintosh file |   4.00 KB    | QSIS_DISK | 2025-01-26 14:18:00 |
    | 1 |          /Volumes/QSIS_DISK/QSIS-Server-run/run_info.yml          |             ASCII text             |    101 B     | QSIS_DISK | 2022-06-27 23:55:45 |
    | 2 |     /Volumes/QSIS_DISK/qsis-server-inspect/data/run_info.yml      |             ASCII text             |   2.46 KB    | QSIS_DISK | 2023-03-18 02:08:30 |
    | 3 |           /Volumes/QSIS_DISK/line-bot-qsis/config.yaml            |             ASCII text             |    140 B     | QSIS_DISK | 2023-01-14 17:21:30 |
    | 4 |  /Volumes/QSIS_DISK/event_data_download_waveform_api/config.yaml  |      Unicode text, UTF-8 text      |    511 B     | QSIS_DISK | 2025-01-25 12:51:35 |
    +---+-------------------------------------------------------------------+------------------------------------+--------------+-----------+---------------------+

    🔍 Best fuzzy match:
    +---+----------------------------------------------------------+------------+--------------+-----------+---------------------+
    |   |                           Path                           | File Kind  | Size (bytes) |  Volume   |    Modified Time    |
    +---+----------------------------------------------------------+------------+--------------+-----------+---------------------+
    | 0 | /Volumes/QSIS_DISK/qsis-server-inspect/location_info.yml | ASCII text |   1.10 KB    | QSIS_DISK | 2023-04-07 22:32:39 |
    +---+----------------------------------------------------------+------------+--------------+-----------+---------------------+
    Enter filename to search: wpa_supplicant.conf

    ✅ Exact match found:
    +---+----------------------------------------+------------+--------------+-----------+---------------------+
    |   |                  Path                  | File Kind  | Size (bytes) |  Volume   |    Modified Time    |
    +---+----------------------------------------+------------+--------------+-----------+---------------------+
    | 0 | /Volumes/QSIS_DISK/wpa_supplicant.conf | ASCII text |    161 B     | QSIS_DISK | 2022-03-30 20:18:02 |
    +---+----------------------------------------+------------+--------------+-----------+---------------------+
    ```

## 🏆 Contributors
- Utpal Kumar - Developer & Maintainer
- Contributions are welcome! Feel free to open an issue or submit a PR.