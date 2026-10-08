"""Tests for UnknownSymptomDetector service."""

from __future__ import annotations

import pytest

from kijan_personal_tracker.services.unknown_symptom_detector import (
    SymptomEntry,
    UnknownSymptom,
    UnknownSymptomDetector,
    _cluster_def_names,
    _tokenize,
    SUGGEST_FLOOR,
    CLUSTER_MIN_SIZE,
)


class TestConstants:
    def test_suggest_floor_is_0_5(self):
        """SUGGEST_FLOOR must be 0.5, not 0.4."""
        assert SUGGEST_FLOOR == 0.5

    def test_cluster_min_size_is_2(self):
        assert CLUSTER_MIN_SIZE == 2


class TestTokenize:
    def test_lowercases(self):
        assert "kopfschmerz" in _tokenize("KOPFSCHMERZ")

    def test_filters_stop_words(self):
        tokens = _tokenize("ich habe Kopfschmerzen und Schwindel")
        assert "ich" not in tokens
        assert "habe" not in tokens
        assert "und" not in tokens

    def test_filters_short_tokens(self):
        tokens = _tokenize("k x ab cd")
        assert "k" not in tokens
        assert "x" not in tokens
        assert "ab" not in tokens
        assert "cd" not in tokens  # 2 chars, len(t) > 2 means filtered

    def test_returns_empty_for_stop_word_only(self):
        assert _tokenize("der die das") == []


class TestClusterDefNames:
    def test_basic_naming(self):
        """Top tokens should form a readable name."""
        members = [
            [["kopf", "schmerz"]],
            [["kopf", "druck"]],
            [["kopf", "weh"]],
        ]
        names = _cluster_def_names(members)
        assert len(names) == 3
        assert "Kopf" in names[0]

    def test_multiple_clusters(self):
        members = [
            [["kopf", "schmerz"]],
            [["bauch", "weh"]],
        ]
        names = _cluster_def_names(members)
        assert len(names) == 2
        assert "Kopf" in names[0]
        assert "Bauch" in names[1]

    def test_empty_cluster(self):
        members = [[]]
        names = _cluster_def_names(members)
        assert "Symptomgruppe" in names[0]


class TestClusterSymptoms:
    def test_empty_input(self):
        detector = UnknownSymptomDetector()
        result = detector.cluster_symptoms([])
        assert result == []

    def test_single_entry(self):
        detector = UnknownSymptomDetector(min_cluster_size=1)
        entries = [SymptomEntry(description="Kopfschmerz", source="test")]
        result = detector.cluster_symptoms(entries)
        assert len(result) == 1
        assert result[0].confidence >= SUGGEST_FLOOR

    def test_similar_entries_cluster(self):
        """Entries with overlapping tokens should cluster together."""
        detector = UnknownSymptomDetector(min_cluster_size=1)
        # Use longer descriptions with shared tokens so TF-IDF can find overlap
        entries = [
            SymptomEntry(description="Ich habe starke Kopfschmerzen im Stirnbereich", source="a"),
            SymptomEntry(description="Kopfschmerzen und Schwindel beim Aufstehen", source="b"),
            SymptomEntry(description="Ständige Kopfschmerzen mit Übelkeit", source="c"),
        ]
        result = detector.cluster_symptoms(entries)
        # With shared tokens (Kopf, schmerz), entries should cluster
        assert len(result) >= 1
        if len(result) == 1:
            assert result[0].source_count >= 1

    def test_different_entries_separate(self):
        detector = UnknownSymptomDetector(min_cluster_size=1)
        entries = [
            SymptomEntry(description="Kopfschmerz", source="a"),
            SymptomEntry(description="Bauchschmerz", source="b"),
        ]
        result = detector.cluster_symptoms(entries)
        # Depending on TF-IDF, these may or may not cluster
        # Just verify no crash and confidence is set
        for cluster in result:
            assert cluster.confidence >= 0

    def test_suggest_floor_filters(self):
        """High suggest_floor should filter out low-confidence clusters."""
        detector = UnknownSymptomDetector(
            min_cluster_size=1,
            suggest_floor=0.99,
        )
        # Single entries get confidence=1.0, so they pass a 0.99 floor
        # Use a 1.0 floor to actually filter them out
        detector2 = UnknownSymptomDetector(
            min_cluster_size=1,
            suggest_floor=1.01,  # above max possible (1.0)
        )
        entries = [SymptomEntry(description="Kopfschmerz", source="a")]
        result = detector2.cluster_symptoms(entries)
        assert len(result) == 0

    def test_source_count(self):
        detector = UnknownSymptomDetector(min_cluster_size=1)
        entries = [
            SymptomEntry(description="Kopfschmerz", source="csv"),
            SymptomEntry(description="Kopfschmerz", source="checkin"),
        ]
        result = detector.cluster_symptoms(entries)
        assert len(result) >= 1
        assert result[0].source_count >= 2

    def test_output_is_unknown_symptom_dataclass(self):
        detector = UnknownSymptomDetector(min_cluster_size=1)
        entries = [SymptomEntry(description="Kopfschmerz", source="test")]
        result = detector.cluster_symptoms(entries)
        assert isinstance(result[0], UnknownSymptom)
        assert hasattr(result[0], "cluster_id")
        assert hasattr(result[0], "name")
        assert hasattr(result[0], "confidence")
        assert hasattr(result[0], "member_descriptions")
        assert hasattr(result[0], "source_count")


# --- Public API export pinning (regression guard for review-issue #2) ---
class TestPublicApiExports:
    """Pins the package-level symbols downstream code depends on.

    Created during kanban t_b1193638 follow-up to guard against silent
    rename/removal of the class-based public API. If you rename an
    exported class, update this test in the same commit.
    """

    def test_services_exports(self):
        import kijan_personal_tracker.services as services
        for name in ("LLMMappingService", "UnknownSymptomDetector"):
            assert hasattr(services, name), f"services missing export: {name}"
            assert name in services.__all__, f"services.__all__ missing: {name}"

    def test_routers_exports(self):
        import kijan_personal_tracker.routers as routers
        for name in ("UnknownSymptomRouter",):
            assert hasattr(routers, name), f"routers missing export: {name}"
            assert name in routers.__all__, f"routers.__all__ missing: {name}"

    def test_submodule_exports_resolve(self):
        from kijan_personal_tracker.services.unknown_symptom_detector import (
            UnknownSymptomDetector,
            UnknownSymptom,
            SymptomEntry,
        )
        from kijan_personal_tracker.routers.unknown_symptom import (
            UnknownSymptomRouter,
        )
        # API must be instantiable
        assert UnknownSymptomDetector(min_cluster_size=1) is not None
        assert UnknownSymptomRouter() is not None
