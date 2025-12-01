"""DBSCAN clustering implementation for PhotoCluster."""

import logging

import numpy as np
from sklearn.cluster import DBSCAN

from .models.image import ClusteredImage, ImageHash

logger = logging.getLogger(__name__)

MIN_SAMPLES = 2


def cluster_hashes(hash_data: list[ImageHash], eps: float) -> list[ClusteredImage]:
    """Cluster hashes using DBSCAN with Hamming distance.

    Args:
        hash_data: List of ImageHash objects
        eps: DBSCAN epsilon parameter as proportion (0.0-1.0).
             Represents the maximum proportion of differing bits for images
             to be considered similar. Lower = stricter clustering.

    Returns:
        List of ClusteredImage objects with path and cluster label
    """
    if not hash_data:
        logger.warning("No hash data provided for clustering")
        return []

    logger.info(f"Clustering {len(hash_data)} images with eps={eps}")

    vectors = np.stack([result.hash for result in hash_data])

    db = DBSCAN(eps=eps, min_samples=MIN_SAMPLES, metric="hamming")
    labels = db.fit_predict(vectors)

    num_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    num_noise = list(labels).count(-1)
    logger.info(
        f"Clustering complete: {num_clusters} clusters, {num_noise} noise points"
    )

    return [
        ClusteredImage(path=result.path, cluster_id=int(label))
        for result, label in zip(hash_data, labels, strict=True)
    ]
