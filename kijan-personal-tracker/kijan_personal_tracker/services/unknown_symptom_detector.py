"""UnknownSymptomDetector: clusters raw symptom descriptions from multiple import sources
into named symptom clusters with confidence scores.

The detector uses TF-IDF vectorization + k-means clustering to group similar
symptom reports.  Each cluster is assigned a human-readable name derived from
the most frequent tokens in that cluster.

SUGGEST_FLOOR = 0.5
    Minimum confidence threshold for generating an automatic suggestion.
    Clusters below this floor are still stored in the database but are NOT
    surfaced to the user as actionable items.  The value 0.5 was chosen as a
    pragmatic balance between recall (catching real patterns) and precision
    (avoiding false-positive suggestions that would annoy the user).
"""

from __future__ import annotations

import math
import logging
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Iterable

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Minimum combined score for an "unknown" symptom to surface a suggestion.
# 0.5 chosen so single-token typos (Levenshtein ≈ 1 − 1/|needle|) stay above
# this floor while clearly-unrelated symptoms (e.g. "Rage attacks") fall below
# it and emit suggestions=[]. Tuned via USD-TST-004..006 in
# kpt-doc/_specs/health-aggregation-layer/import/unknown-symptom-detector.md.
SUGGEST_FLOOR = 0.5
# Minimum number of cluster members before we treat a cluster as a real
# recurring unknown symptom rather than noise from a single CSV import.
CLUSTER_MIN_SIZE = 2  # ignore clusters with fewer members


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class SymptomEntry:
    """A single raw symptom report from any import source."""

    description: str
    source: str  # e.g. "daily_checkin", "import_csv"
    timestamp: str | None = None


@dataclass
class UnknownSymptom:
    """A discovered cluster of similar symptom reports."""

    cluster_id: int
    name: str
    confidence: float
    member_descriptions: list[str] = field(default_factory=list)
    source_count: int = 0


# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------

_STOP_WORDS = frozenset({
    "der", "die", "das", "den", "dem", "des", "ein", "eine", "einer",
    "einem", "eines", "ich", "du", "er", "sie", "es", "wir", "ihr",
    "und", "oder", "aber", "auch", "noch", "schon", "mal", "hat",
    "hatte", "war", "ist", "sind", "war", "habe", "kann", "muss",
    "will", "soll", "wird", "nur", "nicht", "kein", "keine", "mit",
    "ohne", "für", "nach", "bei", "seit", "bis", "vor", "auf",
    "zwischen", "über", "unter", "an", "in", "aus", "bei", "da",
    "wenn", "dass", "wie", "was", "wer", "wo", "denn", "so",
    "sehr", "mehr", "weniger", "ziemlich", "etwa", "etwas", "viel",
    "ganz", "total", "komplett", "ganz", "absolut", "einfach",
    "plötzlich", "ständig", "immer", "oft", "manchmal", "selten",
    "plötzlich", "langsam", "schnell", "stetig", "kontinuierlich",
    "seit", "vor", "bis", "während", "gegen", "um", "durch",
})


def _tokenize(text: str) -> list[str]:
    """Lowercase, strip punctuation, filter stop words & short tokens."""
    text = text.lower()
    tokens = re.findall(r"[a-zäöüß]+", text)
    return [t for t in tokens if t not in _STOP_WORDS and len(t) > 2]


# ---------------------------------------------------------------------------
# TF-IDF helpers (lightweight, no external deps)
# ---------------------------------------------------------------------------


def _compute_idf(documents: list[list[str]]) -> dict[str, float]:
    """Compute IDF for a list of tokenized documents."""
    n_docs = len(documents)
    doc_freq: Counter = Counter()
    for doc in documents:
        for token in set(doc):
            doc_freq[token] += 1
    idf: dict[str, float] = {}
    for token, df in doc_freq.items():
        idf[token] = math.log((1 + n_docs) / (1 + df)) + 1
    return idf


def _tf_vector(tokens: list[str]) -> dict[str, float]:
    """Term frequency vector for a single document."""
    counts = Counter(tokens)
    total = len(tokens)
    if total == 0:
        return {}
    return {token: count / total for token, count in counts.items()}


def _cosine_sim(a: dict[str, float], b: dict[str, float]) -> float:
    """Cosine similarity between two sparse vectors."""
    dot = sum(a.get(t, 0) * b.get(t, 0) for t in set(a) & set(b))
    norm_a = math.sqrt(sum(v * v for v in a.values()))
    norm_b = math.sqrt(sum(v * v for v in b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


# ---------------------------------------------------------------------------
# Agglomerative clustering (simple, no sklearn dependency)
# ---------------------------------------------------------------------------


def _agglomerative_cluster(
    vectors: list[dict[str, float]],
    threshold: float = 0.35,
) -> list[list[int]]:
    """Group indices by cosine similarity using agglomerative clustering.

    Clusters are formed bottom-up: items with cosine similarity >= threshold
    are merged.  Returns a list of clusters, each cluster being a list of
    original indices.
    """
    n = len(vectors)
    if n == 0:
        return []

    # Each item starts as its own cluster
    clusters: list[list[int]] = [[i] for i in range(n)]

    # Iteratively merge the closest pair
    while len(clusters) > 1:
        best_sim = -1.0
        best_i = best_j = -1

        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                # Merge vectors in each cluster
                vec_i: dict[str, float] = defaultdict(float)
                vec_j: dict[str, float] = defaultdict(float)
                for idx in clusters[i]:
                    for t, v in vectors[idx].items():
                        vec_i[t] += v
                for idx in clusters[j]:
                    for t, v in vectors[idx].items():
                        vec_j[t] += v
                sim = _cosine_sim(dict(vec_i), dict(vec_j))
                if sim > best_sim:
                    best_sim = sim
                    best_i = i
                    best_j = j

        if best_sim < threshold:
            break

        clusters[best_i].extend(clusters.pop(best_j))

    return clusters


# ---------------------------------------------------------------------------
# Cluster naming
# ---------------------------------------------------------------------------


def _cluster_def_names(cluster_members: list[list[list[str]]]) -> dict[int, str]:
    """Assign a human-readable name to each cluster using frequency analysis.

    For each cluster, the most common tokens (excluding stop words) that form
    a meaningful phrase are extracted.  The resulting name is a short,
    descriptive string suitable for display.

    Args:
        cluster_members: list of clusters, each cluster is a list of tokenized
            member lists.

    Returns:
        A dict mapping cluster index to name.
    """
    names: dict[int, str] = {}
    for idx, members in enumerate(cluster_members):
        all_tokens: Counter = Counter()
        for tokens in members:
            all_tokens.update(tokens)
        # Top-3 most frequent tokens
        top = all_tokens.most_common(3)
        if top:
            # Form a name from the top tokens
            name = " + ".join(t.capitalize() for t, _ in top if len(t) > 3)
        else:
            name = f"Symptomgruppe {idx + 1}"
        names[idx] = name
    return names


# ---------------------------------------------------------------------------
# Main detector
# ---------------------------------------------------------------------------


class UnknownSymptomDetector:
    """Detects and clusters unknown / novel symptoms from raw reports.

    The detector is stateless — pass all symptom entries at once to
    :meth:`cluster_symptoms`.  This is intentional: the clustering operates
    over the full corpus to produce globally consistent clusters.
    """

    def __init__(
        self,
        cluster_threshold: float = 0.35,
        suggest_floor: float = SUGGEST_FLOOR,
        min_cluster_size: int = CLUSTER_MIN_SIZE,
    ) -> None:
        self.cluster_threshold = cluster_threshold
        self.suggest_floor = suggest_floor
        self.min_cluster_size = min_cluster_size

    def cluster_symptoms(
        self,
        symptoms: Iterable[SymptomEntry],
    ) -> list[UnknownSymptom]:
        """Cluster raw symptom entries and return named UnknownSymptom objects.

        Args:
            symptoms: Iterable of :class:`SymptomEntry` objects.

        Returns:
            A list of :class:`UnknownSymptom` objects, one per cluster.
            Clusters smaller than ``min_cluster_size`` are excluded.
        """
        entries = list(symptoms)
        if not entries:
            return []

        # Tokenize all entries
        tokenized: list[list[str]] = [_tokenize(e.description) for e in entries]

        # Build TF-IDF vectors
        idf = _compute_idf(tokenized)

        tf_vectors: list[dict[str, float]] = []
        for tokens in tokenized:
            tf = _tf_vector(tokens)
            # Apply IDF weighting
            idf_vec: dict[str, float] = {}
            for token, tf_val in tf.items():
                idf_val = idf.get(token, 1.0)
                idf_vec[token] = tf_val * idf_val
            tf_vectors.append(idf_vec)

        # Cluster
        raw_clusters = _agglomerative_cluster(tf_vectors, self.cluster_threshold)

        # Build UnknownSymptom objects
        results: list[UnknownSymptom] = []
        cluster_members_by_idx: list[list[list[str]]] = []

        for cluster_idx, member_indices in enumerate(raw_clusters):
            if len(member_indices) < self.min_cluster_size:
                continue

            members: list[str] = []
            sources: set[str] = set()
            for i in member_indices:
                members.append(entries[i].description)
                sources.add(entries[i].source)

            # Compute confidence as average pairwise similarity within cluster
            # For single-entry clusters, assign a default confidence of 1.0
            # (the entry is a perfect match with itself).
            sims: list[float] = []
            for a in range(len(member_indices)):
                for b in range(a + 1, len(member_indices)):
                    sims.append(
                        _cosine_sim(
                            tf_vectors[member_indices[a]],
                            tf_vectors[member_indices[b]],
                        )
                    )
            avg_confidence = (sum(sims) / len(sims)) if len(sims) > 1 else 1.0

            cluster_members_by_idx.append(
                [_tokenize(m) for m in members]
            )
            results.append(UnknownSymptom(
                cluster_id=cluster_idx,
                name="",  # placeholder — set below
                confidence=round(avg_confidence, 4),
                member_descriptions=members,
                source_count=len(sources),
            ))

        # Assign human-readable names
        def_names = _cluster_def_names(cluster_members_by_idx)
        for name_idx, unknown_symptom in enumerate(results):
            unknown_symptom.name = def_names.get(name_idx, f"Symptomgruppe {name_idx + 1}")

        # Filter by suggestion floor
        results = [
            s for s in results
            if s.confidence >= self.suggest_floor
        ]

        logger.info(
            "UnknownSymptomDetector: %d clusters from %d entries, %d above suggest_floor",
            len(results),
            len(entries),
            len(results),
        )

        return results
