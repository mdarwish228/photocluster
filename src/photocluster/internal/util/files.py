"""File utilities for PhotoCluster."""

import shutil
from itertools import chain
from pathlib import Path

from ..models.image import ClusteredImage

IMAGE_FILE_PATTERNS = ["*.jpg", "*.jpeg"]


def find_image_files(directory: Path) -> list[Path]:
    """Find all image files (JPEG) in a directory recursively.

    Args:
        directory: Directory to search for images

    Returns:
        List of Path objects pointing to image files
    """
    return list(chain.from_iterable(directory.rglob(p) for p in IMAGE_FILE_PATTERNS))


def group_image_files(clustered_images: list[ClusteredImage], out_dir: Path) -> None:
    """Organize images into cluster-based subdirectories.

    Files are moved (not copied) to their respective cluster folders.

    Args:
        clustered_images: List of ClusteredImage objects with path and cluster_id
        out_dir: Output directory root
    """
    out_path = out_dir
    out_path.mkdir(parents=True, exist_ok=True)

    UNIQUE_CLUSTER_ID = -1

    for clustered in clustered_images:
        if clustered.cluster_id == UNIQUE_CLUSTER_ID:
            continue
        cluster_name = f"group_{clustered.cluster_id}"
        cluster_dir = out_path / cluster_name
        cluster_dir.mkdir(parents=True, exist_ok=True)

        destination = cluster_dir / clustered.path.name
        shutil.move(str(clustered.path), str(destination))
