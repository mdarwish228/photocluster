"""Image hash computation with multiprocessing."""

import multiprocessing
from pathlib import Path

from ..models.image import ImageHash
from ..util.files import find_image_files
from .jpeg import JPEGHasher


class Hasher:
    """Main hasher that routes to appropriate hasher based on file extension."""

    def __init__(self):
        """Initialize the hasher with supported hashers."""
        self._hashers = [JPEGHasher]

    def __call__(self, path: Path) -> ImageHash:
        """Route to appropriate hasher based on file extension.

        Args:
            path: Path to the image file

        Returns:
            ImageHash object containing the hash and path

        Raises:
            ValueError: If no hasher can process the file
        """
        for hasher_class in self._hashers:
            if hasher_class.can_hash(path):
                return hasher_class.hash(path)
        raise ValueError(f"No hasher available for file: {path}")


def compute_hashes(
    img_dir: Path,
    num_processes: int,
) -> list[ImageHash]:
    """Scan a directory and compute perceptual hashes using the provided hasher.

    Args:
        img_dir: Directory containing images to process
        num_processes: Number of worker processes to spawn
        hasher: Hasher instance (defaults to Hasher which auto-routes)

    Returns:
        List of ImageHash objects
    """

    paths = find_image_files(img_dir)

    if not paths:
        return []

    with multiprocessing.Pool(processes=num_processes) as pool:
        hashes = pool.map(Hasher(), paths)

    return hashes
