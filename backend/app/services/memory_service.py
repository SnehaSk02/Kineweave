from sqlalchemy.orm import Session

from app.models.capture import Capture
from app.services.vector_store import (
    search_memory
)


def find_related_memories(
    query: str,
    db: Session
):

    results = search_memory(
        query=query,
        n_results=10
    )

    ids = results["ids"][0]

    distances = results["distances"][0]

    captures = []

    for capture_id, distance in zip(
        ids,
        distances
    ):

        # Ignore weak matches
        if distance > 1.2:
            continue

        capture = db.query(
            Capture
        ).filter(
            Capture.id == int(capture_id)
        ).first()

        if capture:

            captures.append(
                {
                    "capture": capture,
                    "distance": distance
                }
            )

    captures.sort(
    key=lambda x: x["distance"]
    )
    return captures
    