"""DBSCAN clustering implementation for PhotoCluster."""

import numpy as np
from sklearn.cluster import DBSCAN

from .models.image import ClusteredImage, ImageHash

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
        return []

    vectors = np.stack([result.hash for result in hash_data])

    db = DBSCAN(eps=eps, min_samples=MIN_SAMPLES, metric="hamming")
    labels = db.fit_predict(vectors)

    return [
        ClusteredImage(path=result.path, cluster_id=int(label))
        for result, label in zip(hash_data, labels, strict=True)
    ]
