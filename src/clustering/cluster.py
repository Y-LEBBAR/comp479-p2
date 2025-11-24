import os
import json
import numpy as np #https://pypi.org/project/numpy/2.3.5/
from sklearn.feature_extraction.text import TfidfVectorizer #https://pypi.org/project/scikit-learn/1.7.2/
from sklearn.cluster import KMeans

from index.storage import load_index_json


class ClusterEngine:
    """
    Handles TF-IDF vectorization and K-Means clustering on the indexed documents.
    """

    def __init__(self, index_path: str = "data/index.json"):
        self.index, self.docs_meta = load_index_json(index_path)

        # Reconstruct corpus as one string per document
        self.corpus = self._build_corpus()

        # TF-IDF vectorizer (configure for medium-sized academic texts)
        self.vectorizer = TfidfVectorizer(
            max_df=0.85,
            min_df=1,
            stop_words="english",
            lowercase=True
        )

        # TF-IDF matrix (will be computed in vectorize())
        self.tfidf_matrix = None
        self.feature_names = None

    def _build_corpus(self) -> list[str]:
        """
        Convert the inverted index back into a list of full document strings.
        Each doc is reconstructed from all tokens that appear in it.
        """
        # docs_meta keys may be string or int — normalize
        doc_ids = list(self.docs_meta.keys())
        doc_ids = [int(i) for i in doc_ids]

        # Build token lists for each document
        doc_tokens = {doc_id: [] for doc_id in doc_ids}

        for token, postings in self.index.items():
            for doc_id, freq in postings.items():
                # Append token 'freq' times (rebuild the document text)
                doc_id = int(doc_id)
                doc_tokens[doc_id].extend([token] * freq)

        # Convert tokens back into strings
        corpus = [" ".join(doc_tokens[doc_id]) for doc_id in doc_ids]
        return corpus

    def vectorize(self):
        """
        Compute the TF-IDF matrix for the corpus.
        """
        if not self.corpus:
            raise ValueError("Corpus is empty — ensure documents were indexed.")

        self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus)
        self.feature_names = self.vectorizer.get_feature_names_out()

    def run_kmeans(self, k: int, output_dir: str):
        """
        Run K-Means clustering with k clusters.
        Save results to 'output_dir'.
        """
        if self.tfidf_matrix is None:
            raise RuntimeError("Call vectorize() before running clustering.")

        os.makedirs(output_dir, exist_ok=True)

        kmeans = KMeans(n_clusters=k, n_init="auto", random_state=42)
        labels = kmeans.fit_predict(self.tfidf_matrix)

        # Save cluster assignments
        self._save_cluster_assignments(labels, output_dir)

        # Extract and save top terms
        top_terms = self._extract_top_terms(kmeans, top_n=50)
        self._save_top_terms(top_terms, output_dir)

        # Save summary JSON
        summary = {
            "k": k,
            "num_documents": len(labels),
            "clusters": top_terms
        }
        with open(os.path.join(output_dir, "summary.json"), "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

    def _extract_top_terms(self, kmeans_model, top_n=50):
        """
        For each cluster, extract the top-N terms by centroid weight.
        """
        centroids = kmeans_model.cluster_centers_
        top_terms = {}

        for cluster_id, center_vec in enumerate(centroids):
            # Sort term indices by TF-IDF weight in centroid
            top_indices = np.argsort(center_vec)[::-1][:top_n]
            terms = [self.feature_names[i] for i in top_indices]
            top_terms[int(cluster_id)] = terms

        return top_terms

    def _save_cluster_assignments(self, labels, output_dir):
        """
        Save doc_id → cluster assignments.
        """
        path = os.path.join(output_dir, "cluster_assignments.txt")
        with open(path, "w", encoding="utf-8") as f:
            for doc_id, cluster_id in enumerate(labels):
                url = self.docs_meta[str(doc_id)]["url"]
                f.write(f"{doc_id}\tCluster {cluster_id}\t{url}\n")

    def _save_top_terms(self, top_terms, output_dir):
        """
        Save top-50 terms for each cluster.
        """
        path = os.path.join(output_dir, "top_terms.txt")
        with open(path, "w", encoding="utf-8") as f:
            for cluster_id, terms in top_terms.items():
                f.write(f"=== Cluster {cluster_id} ===\n")
                for t in terms:
                    f.write(f"{t}\n")
                f.write("\n")


def run_all_clusters(index_path="data/index.json"):
    """
    Run TF-IDF → KMeans for k = 2, 10, 20.
    """
    engine = ClusterEngine(index_path)
    engine.vectorize()

    cluster_settings = {
        2:  "data/clusters/k2",
        10: "data/clusters/k10",
        20: "data/clusters/k20"
    }

    for k, outdir in cluster_settings.items():
        print(f"\n=== Running K-Means (k={k}) ===")
        engine.run_kmeans(k, outdir)
        print(f"Saved results to: {outdir}")


if __name__ == "__main__":
    run_all_clusters()
