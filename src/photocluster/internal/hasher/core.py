"""Image hash computation with multiprocessing."""

import logging
import multiprocessing
from pathlib import Path

from ..models.image import ImageHash
from ..util.files import find_image_files
from .jpeg import JPEGHasher

logger = logging.getLogger(__name__)


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
                logger.debug(f"Computing hash for {path.name}")
                return hasher_class.hash(path)
        logger.error(f"No hasher available for file: {path}")
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
    logger.info(f"Scanning directory for images: {img_dir}")
    paths = find_image_files(img_dir)

    if not paths:
        logger.warning("No image files found in directory")
        return []

    logger.info(f"Found {len(paths)} image files")
    logger.info(f"Computing hashes using {num_processes} processes")

    with multiprocessing.Pool(processes=num_processes) as pool:
        hashes = pool.map(Hasher(), paths)

    logger.info(f"Successfully computed {len(hashes)} hashes")
    return hashes
