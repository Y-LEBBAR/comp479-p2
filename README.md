# COMP 479 – Project 2  
## Information Retrieval Pipeline + Clustering

This README explains how to install, run, and reproduce the results for the full crawling, indexing, and clustering pipeline.  
All instructions assume **Windows + PowerShell**, **Python 3.11**, and running inside a **virtual environment (.venv)**.

---

# 1. Project Structure

```
project_2/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── index.json                 # generated after running main.py
│   └── clusters/
│       ├── k2/                    # generated
│       ├── k10/                   # generated
│       └── k20/                   # generated
│
├── report/                        # PDF report
│
├── src/
│   ├── main.py                    # full crawling + indexing pipeline
│   │
│   ├── crawler/
│   │   ├── __init__.py
│   │   ├── crawler.py
│   │   ├── robots.py
│   │   └── utils.py
│   │
│   ├── index/
│   │   ├── __init__.py
│   │   ├── tokenizer.py
│   │   ├── indexer.py
│   │   ├── pdf_extractor.py
│   │   └── storage.py
│   │
│   ├── clustering/
│   │   ├── __init__.py
│   │   └── cluster.py             # runs TF-IDF + K-Means for k = 2,10,20
│   │
│   └── queries/
│       ├── __init__.py
│       └── run_queries.py         # not part of core grading, optional
│
└── tests/                         # unit tests for crawling + indexing
```

---

# 2. Setup Instructions

## 2.1 Create and activate the virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

## 2.2 Install dependencies

```powershell
pip install -r requirements.txt
```

### Package versions used for reproducibility:

```
beautifulsoup4==4.12.3
requests==2.32.3
scikit-learn==1.5.1
numpy==1.26.4
PyPDF2==3.0.1
```

---

# 3. Running the Crawling + Indexing Pipeline

The main pipeline:

1. Crawls starting at:  
   `https://spectrum.library.concordia.ca/`
2. Collects up to **max_files** PDF URLs  
3. Downloads PDFs  
4. Extracts text  
5. Tokenizes text  
6. Builds a positional inverted index  
7. Saves results to `data/index.json`

## Run it using:

```powershell
python src/main.py
```

### Configuration (inside `main.py`):

```python
seed_url = "https://spectrum.library.concordia.ca/"
max_files = 50               # modify to increase limit
output_path = "data/index.json"
```

### Output created:

```
data/index.json
```

This file contains:

- Vocabulary  
- Per-document term frequencies  
- Document list  
- Total frequency counts  

---

# 4. Running the Clustering

Clustering uses:

- `sklearn.feature_extraction.text.TfidfVectorizer`
- `sklearn.cluster.KMeans`

You must first run **main.py** before clustering (to generate `index.json`).

### Run clustering:

```powershell
python src/clustering/cluster.py
```

This will generate results for:

- k = 2  
- k = 10  
- k = 20  

### Outputs:

```
data/clusters/k2/
data/clusters/k10/
data/clusters/k20/

Each contains:
    cluster_assignments.txt         # indicates which cluster each pdf file was assigned to
    top_terms.txt                   
    summary.json                    
```

### Notes for markers:

- `top_terms.txt` contains the **top 50 TF-IDF terms** for each cluster (highest weights).
- `summary.json` contains most frequent terms in each cluster in a json format.
- All terms and ranks are computed directly from the TF-IDF matrices.

---

# 5. Running Unit Tests (Note: these were made for me I don't see why you would need to run them but they are here in case)

To run the full test suite:

```powershell
python -m unittest discover -s tests
```

Tests cover:

- Robots.txt parsing  
- URL normalization  
- PDF extraction  
- Tokenization  
- Index building  
- End-to-end pipeline integration  

---

# 6. Reproducibility Notes

### Robots.txt  
Spectrum blocks most crawling paths.  
The crawler automatically respects `robots.txt` using `robots.py`:  
https://www.rfc-editor.org/rfc/rfc9309

### Deterministic Clustering  
`random_state = 42` for each K-Means run.

### File overwriting  
Running `main.py` again overwrites:

```
data/index.json
```

Running `cluster.py` again overwrites:

```
data/clusters/k2/
data/clusters/k10/
data/clusters/k20/
```

# End of README
