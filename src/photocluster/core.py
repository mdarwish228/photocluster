"""Convenience function for photo clustering."""

from pathlib import Path

from .internal.cluster import cluster_hashes
from .internal.hasher.core import compute_hashes
from .internal.models.validation import PhotoclusterInputs
from .internal.util.files import group_image_files
from .internal.util.processing import get_num_processes


def photocluster(input_dir: str | Path, sensitivity: float) -> None:
    """Perform photo clustering and grouping operation.

    Images will be organized into cluster subdirectories within the input directory.
    Files are moved (not copied) to their respective cluster folders.

    Args:
        input_dir: Directory containing images to cluster (str or Path)
        sensitivity: Clustering sensitivity as proportion (0.0-1.0).
    """
    input_path = Path(input_dir) if isinstance(input_dir, str) else input_dir
    input = PhotoclusterInputs(input_dir=input_path, sensitivity=sensitivity)

    num_processes = get_num_processes()
    hash_data = compute_hashes(
        input.input_dir,
        num_processes=num_processes,
    )

    clustered_images = cluster_hashes(hash_data, eps=input.sensitivity)

    group_image_files(clustered_images, input.input_dir)
