"""Tests for hasher core module."""

import pytest
from PIL import Image

from photocluster.internal.hasher.core import Hasher, compute_hashes
from photocluster.internal.models.image import ImageHash


class TestHasher:
    """Tests for Hasher routing class."""

    def test_hasher_initialization(self):
        """Test Hasher can be instantiated."""
        hasher = Hasher()
        assert hasher is not None

    def test_hasher_routes_jpg_to_jpeg_hasher(self, temp_dir):
        """Test Hasher routes .jpg files to JPEGHasher."""
        img_path = temp_dir / "test.jpg"
        Image.new("RGB", (10, 10)).save(img_path, "JPEG")

        hasher = Hasher()
        result = hasher(img_path)

        assert isinstance(result, ImageHash)
        assert result.path == img_path

    def test_hasher_routes_jpeg_to_jpeg_hasher(self, temp_dir):
        """Test Hasher routes .jpeg files to JPEGHasher."""
        img_path = temp_dir / "test.jpeg"
        Image.new("RGB", (10, 10)).save(img_path, "JPEG")

        hasher = Hasher()
        result = hasher(img_path)

        assert isinstance(result, ImageHash)
        assert result.path == img_path

    def test_hasher_handles_unsupported_file_type(self, temp_dir):
        """Test Hasher behavior with unsupported file type."""
        txt_path = temp_dir / "test.txt"
        txt_path.write_text("not an image")

        hasher = Hasher()
        # Hasher should raise ValueError for unsupported file types
        with pytest.raises(ValueError, match="No hasher available"):
            hasher(txt_path)


class TestComputeHashes:
    """Tests for compute_hashes function."""

    def test_compute_hashes_returns_list(self, temp_dir):
        """Test compute_hashes returns a list."""
        img1 = temp_dir / "img1.jpg"
        img2 = temp_dir / "img2.jpg"
        Image.new("RGB", (10, 10)).save(img1, "JPEG")
        Image.new("RGB", (10, 10)).save(img2, "JPEG")

        result = compute_hashes(temp_dir, num_processes=1)

        assert isinstance(result, list)

    def test_compute_hashes_returns_image_hashes(self, temp_dir):
        """Test compute_hashes returns ImageHash objects."""
        img1 = temp_dir / "img1.jpg"
        Image.new("RGB", (10, 10)).save(img1, "JPEG")

        result = compute_hashes(temp_dir, num_processes=1)

        assert len(result) > 0
        assert all(isinstance(h, ImageHash) for h in result)

    def test_compute_hashes_empty_directory(self, temp_dir):
        """Test compute_hashes with empty directory."""
        result = compute_hashes(temp_dir, num_processes=1)

        assert result == []

    def test_compute_hashes_finds_all_images(self, temp_dir):
        """Test compute_hashes finds all images in directory."""
        img1 = temp_dir / "img1.jpg"
        img2 = temp_dir / "img2.jpg"
        img3 = temp_dir / "img3.jpg"
        Image.new("RGB", (10, 10)).save(img1, "JPEG")
        Image.new("RGB", (10, 10)).save(img2, "JPEG")
        Image.new("RGB", (10, 10)).save(img3, "JPEG")

        result = compute_hashes(temp_dir, num_processes=1)

        assert len(result) == 3

    def test_compute_hashes_with_multiprocessing(self, temp_dir):
        """Test compute_hashes works with multiple processes."""
        # Create multiple images
        for i in range(5):
            img = temp_dir / f"img{i}.jpg"
            Image.new("RGB", (10, 10)).save(img, "JPEG")

        result = compute_hashes(temp_dir, num_processes=2)

        assert len(result) == 5
        assert all(isinstance(h, ImageHash) for h in result)

    def test_compute_hashes_recursive_search(self, temp_dir):
        """Test compute_hashes finds images in subdirectories."""
        subdir = temp_dir / "subdir"
        subdir.mkdir()

        img1 = temp_dir / "img1.jpg"
        img2 = subdir / "img2.jpg"
        Image.new("RGB", (10, 10)).save(img1, "JPEG")
        Image.new("RGB", (10, 10)).save(img2, "JPEG")

        result = compute_hashes(temp_dir, num_processes=1)

        assert len(result) == 2
