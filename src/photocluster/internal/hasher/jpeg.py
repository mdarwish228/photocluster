"""JPEG hasher implementation for PhotoCluster."""

from pathlib import Path

import imagehash
import numpy as np
from PIL import Image

from ..models.image import ImageHash
from .base import AbstractHasher

JPEG_EXTENSIONS = [".jpg", ".jpeg"]


class JPEGHasher(AbstractHasher):
    """JPEG image hasher using perceptual hash (phash)."""

    @staticmethod
    def can_hash(path: Path) -> bool:
        """Check if the file is a JPEG image.

        Args:
            path: Path to the image file

        Returns:
            True if the file has a JPEG extension, False otherwise
        """
        return path.suffix.lower() in JPEG_EXTENSIONS

    @staticmethod
    def hash(path: Path) -> ImageHash:
        """Load a JPEG image from a path and compute its perceptual hash as bits.

        Uses phash (perceptual hash) as the hash method.

        Args:
            path: Path to the image file

        Returns:
            ImageHash object containing the hash and path

        Raises:
            IOError: If the image cannot be opened or processed
        """
        img = Image.open(path).convert("RGB")
        hash_bits = imagehash.phash(img).hash.flatten().astype(np.uint8)
        return ImageHash(path=path, hash=hash_bits)
