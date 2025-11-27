"""Image models for PhotoCluster."""

from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass
class ImageHash:
    """Represents a hash result for an image."""

    path: Path
    hash: np.ndarray  # binary vector (uint8 array)


@dataclass
class ClusteredImage:
    """Represents an image with its cluster assignment."""

    path: Path
    cluster_id: int  # Cluster ID (positive int) or -1 for unique/noise
