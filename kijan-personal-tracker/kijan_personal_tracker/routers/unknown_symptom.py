"""FastAPI router for the UnknownSymptomDetector service.

Provides endpoints to submit raw symptom entries and retrieve
clustered unknown-symptom results.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from fastapi import APIRouter, HTTPException


@dataclass
class SymptomSubmitRequest:
    """Request body for submitting a raw symptom entry."""

    description: str
    source: str
    timestamp: str | None = None


@dataclass
class UnknownSymptomResponse:
    """Response model for a single clustered unknown symptom."""

    cluster_id: int
    name: str
    confidence: float
    member_count: int
    sources: list[str]


class UnknownSymptomRouter:
    """FastAPI router that wraps UnknownSymptomDetector."""

    def __init__(self) -> None:
        self.router = APIRouter(prefix="/api/unknown-symptoms", tags=["unknown-symptoms"])
        self._detector: Any = None  # set by app factory

    def set_detector(self, detector: Any) -> None:
        """Inject the UnknownSymptomDetector instance."""
        self._detector = detector

    def register(self) -> APIRouter:
        """Register all routes on the router and return it for mounting."""

        @self.router.post("/cluster")
        async def cluster_symptoms(request: SymptomSubmitRequest) -> dict[str, Any]:
            """Submit a symptom entry and get back any new clusters."""
            if self._detector is None:
                raise HTTPException(status_code=503, detail="Detector not initialized")

            from ..services.unknown_symptom_detector import SymptomEntry

            entry = SymptomEntry(
                description=request.description,
                source=request.source,
                timestamp=request.timestamp,
            )

            clusters = self._detector.cluster_symptoms([entry])
            return {
                "clusters": [
                    {
                        "cluster_id": c.cluster_id,
                        "name": c.name,
                        "confidence": c.confidence,
                        "member_count": len(c.member_descriptions),
                        "sources": list(set(m.source for m in [entry])),
                    }
                    for c in clusters
                ],
            }

        @self.router.get("")
        async def list_clusters() -> dict[str, Any]:
            """List all known unknown-symptom clusters."""
            return {"clusters": []}

        return self.router
