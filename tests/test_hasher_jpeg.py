"""Tests for JPEGHasher."""

import numpy as np
import pytest
from PIL import Image

from photocluster.internal.hasher.jpeg import JPEG_EXTENSIONS, JPEGHasher
from photocluster.internal.models.image import ImageHash


class TestJPEGHasher:
    """Tests for JPEGHasher class."""

    def test_can_hash_jpg_file(self, sample_image_path):
        """Test can_hash returns True for .jpg files."""
        assert JPEGHasher.can_hash(sample_image_path) is True

    def test_can_hash_jpeg_file(self, temp_dir):
        """Test can_hash returns True for .jpeg files."""
        img_path = temp_dir / "test.jpeg"
        Image.new("RGB", (10, 10)).save(img_path, "JPEG")

        assert JPEGHasher.can_hash(img_path) is True

    def test_can_hash_returns_false_for_non_jpeg(self, temp_dir):
        """Test can_hash returns False for non-JPEG files."""
        txt_path = temp_dir / "test.txt"
        txt_path.write_text("not an image")

        assert JPEGHasher.can_hash(txt_path) is False

    def test_can_hash_case_insensitive(self, temp_dir):
        """Test can_hash is case insensitive."""
        img_path = temp_dir / "test.JPG"
        Image.new("RGB", (10, 10)).save(img_path, "JPEG")

        assert JPEGHasher.can_hash(img_path) is True

    def test_hash_returns_image_hash(self, sample_image_path):
        """Test hash method returns ImageHash object."""
        result = JPEGHasher.hash(sample_image_path)

        assert isinstance(result, ImageHash)
        assert result.path == sample_image_path

    def test_hash_returns_numpy_array(self, sample_image_path):
        """Test hash returns numpy array."""
        result = JPEGHasher.hash(sample_image_path)

        assert isinstance(result.hash, np.ndarray)
        assert result.hash.dtype == np.uint8

    def test_hash_has_correct_shape(self, sample_image_path):
        """Test hash array has expected shape."""
        result = JPEGHasher.hash(sample_image_path)

        # phash typically produces 64-bit hash (8x8 array flattened)
        assert len(result.hash) == 64

    def test_hash_different_images_produce_different_hashes(self, temp_dir):
        """Test that different images produce different hashes."""
        img1 = temp_dir / "img1.jpg"
        img2 = temp_dir / "img2.jpg"

        # Create two visually distinct images with different patterns
        # Image 1: Gradient from red to black
        img1_data = Image.new("RGB", (100, 100))
        pixels1 = []
        for _y in range(100):
            for x in range(100):
                r = int(255 * (1 - x / 100))
                pixels1.append((r, 0, 0))
        img1_data.putdata(pixels1)
        img1_data.save(img1, "JPEG")

        # Image 2: Checkerboard pattern
        img2_data = Image.new("RGB", (100, 100))
        pixels2 = []
        for y in range(100):
            for x in range(100):
                if (x // 10 + y // 10) % 2 == 0:
                    pixels2.append((255, 255, 255))
                else:
                    pixels2.append((0, 0, 0))
        img2_data.putdata(pixels2)
        img2_data.save(img2, "JPEG")

        hash1 = JPEGHasher.hash(img1)
        hash2 = JPEGHasher.hash(img2)

        assert not np.array_equal(hash1.hash, hash2.hash)

    def test_hash_same_image_produces_same_hash(self, sample_image_path):
        """Test that same image produces same hash."""
        hash1 = JPEGHasher.hash(sample_image_path)
        hash2 = JPEGHasher.hash(sample_image_path)

        assert np.array_equal(hash1.hash, hash2.hash)

    def test_hash_nonexistent_file_raises_error(self, temp_dir):
        """Test that hashing nonexistent file raises error."""
        nonexistent = temp_dir / "nonexistent.jpg"

        with pytest.raises((IOError, FileNotFoundError, OSError)):
            JPEGHasher.hash(nonexistent)

    def test_jpeg_extensions_constant(self):
        """Test JPEG_EXTENSIONS constant is defined."""
        assert isinstance(JPEG_EXTENSIONS, list)
        assert ".jpg" in JPEG_EXTENSIONS
        assert ".jpeg" in JPEG_EXTENSIONS
