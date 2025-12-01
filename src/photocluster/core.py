"""Convenience function for photo clustering."""

import logging
from pathlib import Path

from .internal.cluster import cluster_hashes
from .internal.hasher.core import compute_hashes
from .internal.models.validation import PhotoclusterInputs
from .internal.util.files import group_image_files
from .internal.util.processing import get_num_processes

logger = logging.getLogger(__name__)


def photocluster(input_dir: str | Path, sensitivity: float = 0.2) -> None:
    """Perform photo clustering and grouping operation.

    Images will be organized into cluster subdirectories within the input directory.
    Files are moved (not copied) to their respective cluster folders.

    Args:
        input_dir: Directory containing images to cluster (str or Path)
        sensitivity: Clustering sensitivity as proportion (0.0-1.0). Defaults to 0.2.
    """
    input_path = Path(input_dir) if isinstance(input_dir, str) else input_dir
    logger.info(f"Starting photo clustering for directory: {input_path}")
    logger.info(f"Using sensitivity: {sensitivity}")

    input = PhotoclusterInputs(input_dir=input_path, sensitivity=sensitivity)

    num_processes = get_num_processes()
    logger.info(f"Using {num_processes} processes for hash computation")

    hash_data = compute_hashes(
        input.input_dir,
        num_processes=num_processes,
    )

    logger.info(f"Computed hashes for {len(hash_data)} images")

    clustered_images = cluster_hashes(hash_data, eps=input.sensitivity)

    num_clusters = len(
        {img.cluster_id for img in clustered_images if img.cluster_id != -1}
    )
    logger.info(f"Created {num_clusters} clusters")

    group_image_files(clustered_images, input.input_dir)

    logger.info("Photo clustering completed")
