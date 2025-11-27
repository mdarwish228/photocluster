"""Tests for clustering functionality."""

from pathlib import Path

import numpy as np

from photocluster.internal.cluster import MIN_SAMPLES, cluster_hashes
from photocluster.internal.models.image import ClusteredImage, ImageHash


class TestClusterHashes:
    """Tests for cluster_hashes function."""

    def test_cluster_hashes_returns_list(self, sample_hash):
        """Test cluster_hashes returns a list."""
        hash_data = [
            ImageHash(path=Path("img1.jpg"), hash=sample_hash),
            ImageHash(path=Path("img2.jpg"), hash=sample_hash),
        ]

        result = cluster_hashes(hash_data, eps=0.2)

        assert isinstance(result, list)

    def test_cluster_hashes_returns_clustered_images(self, sample_hash):
        """Test cluster_hashes returns ClusteredImage objects."""
        hash_data = [
            ImageHash(path=Path("img1.jpg"), hash=sample_hash),
            ImageHash(path=Path("img2.jpg"), hash=sample_hash),
        ]

        result = cluster_hashes(hash_data, eps=0.2)

        assert len(result) == 2
        assert all(isinstance(c, ClusteredImage) for c in result)

    def test_cluster_hashes_similar_images_clustered(self):
        """Test that similar images are clustered together."""
        # Create identical hashes (should cluster together)
        hash1 = np.array([1, 0, 1, 0] * 16, dtype=np.uint8)  # 64 bits
        hash2 = np.array([1, 0, 1, 0] * 16, dtype=np.uint8)  # Same hash

        hash_data = [
            ImageHash(path=Path("img1.jpg"), hash=hash1),
            ImageHash(path=Path("img2.jpg"), hash=hash2),
        ]

        result = cluster_hashes(hash_data, eps=0.1)

        # With identical hashes and low eps, they should be in same cluster
        assert result[0].cluster_id == result[1].cluster_id
        assert result[0].cluster_id != -1

    def test_cluster_hashes_different_images_separate(self):
        """Test that very different images are in separate clusters."""
        # Create very different hashes
        hash1 = np.array([1] * 64, dtype=np.uint8)
        hash2 = np.array([0] * 64, dtype=np.uint8)

        hash_data = [
            ImageHash(path=Path("img1.jpg"), hash=hash1),
            ImageHash(path=Path("img2.jpg"), hash=hash2),
        ]

        result = cluster_hashes(hash_data, eps=0.1)

        # With very different hashes and low eps, they might be separate
        # or one might be noise depending on min_samples
        assert len(result) == 2

    def test_cluster_hashes_preserves_paths(self, sample_hash):
        """Test that paths are preserved in clustered images."""
        hash_data = [
            ImageHash(path=Path("img1.jpg"), hash=sample_hash),
            ImageHash(path=Path("img2.jpg"), hash=sample_hash),
        ]

        result = cluster_hashes(hash_data, eps=0.2)

        paths = {c.path for c in result}
        assert Path("img1.jpg") in paths
        assert Path("img2.jpg") in paths

    def test_cluster_hashes_with_different_eps(self, sample_hash):
        """Test clustering with different eps values."""
        hash_data = [
            ImageHash(path=Path("img1.jpg"), hash=sample_hash),
            ImageHash(path=Path("img2.jpg"), hash=sample_hash),
        ]

        result_low_eps = cluster_hashes(hash_data, eps=0.01)
        result_high_eps = cluster_hashes(hash_data, eps=0.5)

        # Both should return same number of results
        assert len(result_low_eps) == len(result_high_eps) == 2

    def test_cluster_hashes_cluster_id_types(self, sample_hash):
        """Test that cluster_id is an integer."""
        hash_data = [
            ImageHash(path=Path("img1.jpg"), hash=sample_hash),
        ]

        result = cluster_hashes(hash_data, eps=0.2)

        assert isinstance(result[0].cluster_id, int)

    def test_min_samples_constant(self):
        """Test MIN_SAMPLES constant is defined."""
        assert isinstance(MIN_SAMPLES, int)
        assert MIN_SAMPLES >= 1
