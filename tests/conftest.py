"""Pytest configuration and fixtures."""

import shutil
import tempfile
from pathlib import Path

import numpy as np
import pytest
from PIL import Image


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_image_path(temp_dir):
    """Create a sample JPEG image for testing."""
    img_path = temp_dir / "test_image.jpg"
    # Create a simple test image
    img = Image.new("RGB", (100, 100), color="red")
    img.save(img_path, "JPEG")
    return img_path


@pytest.fixture
def sample_hash():
    """Create a sample hash array for testing."""
    return np.array([1, 0, 1, 0, 1, 1, 0, 0], dtype=np.uint8)
