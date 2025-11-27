"""Tests for data models."""

from pathlib import Path

import numpy as np

from photocluster.internal.models.image import ClusteredImage, ImageHash


class TestImageHash:
    """Tests for ImageHash model."""

    def test_image_hash_creation(self, sample_hash):
        """Test creating an ImageHash object."""
        path = Path("test.jpg")
        image_hash = ImageHash(path=path, hash=sample_hash)

        assert image_hash.path == path
        assert np.array_equal(image_hash.hash, sample_hash)

    def test_image_hash_hash_type(self, sample_hash):
        """Test that hash is a numpy array."""
        path = Path("test.jpg")
        image_hash = ImageHash(path=path, hash=sample_hash)

        assert isinstance(image_hash.hash, np.ndarray)
        assert image_hash.hash.dtype == np.uint8


class TestClusteredImage:
    """Tests for ClusteredImage model."""

    def test_clustered_image_creation(self):
        """Test creating a ClusteredImage object."""
        path = Path("test.jpg")
        cluster_id = 5
        clustered = ClusteredImage(path=path, cluster_id=cluster_id)

        assert clustered.path == path
        assert clustered.cluster_id == cluster_id

    def test_clustered_image_unique_id(self):
        """Test ClusteredImage with unique cluster ID (-1)."""
        path = Path("test.jpg")
        clustered = ClusteredImage(path=path, cluster_id=-1)

        assert clustered.cluster_id == -1
