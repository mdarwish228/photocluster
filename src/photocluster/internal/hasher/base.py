"""Abstract base hasher for PhotoCluster."""

from abc import ABC, abstractmethod
from pathlib import Path

from ..models.image import ImageHash


class AbstractHasher(ABC):
    """Abstract base class for image hashers."""

    @staticmethod
    @abstractmethod
    def can_hash(path: Path) -> bool:
        """Check if this hasher can process the given file.

        Args:
            path: Path to the image file

        Returns:
            True if this hasher can process the file, False otherwise
        """
        raise NotImplementedError("Subclasses must implement can_hash method")

    @staticmethod
    @abstractmethod
    def hash(path: Path) -> ImageHash:
        """Compute hash for an image at the given path.

        Args:
            path: Path to the image file

        Returns:
            ImageHash object containing the hash and path

        Raises:
            IOError: If the image cannot be opened or processed
        """
        raise NotImplementedError("Subclasses must implement hash method")
