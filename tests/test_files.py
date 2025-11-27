"""Tests for file utilities."""

from PIL import Image

from photocluster.internal.models.image import ClusteredImage
from photocluster.internal.util.files import find_image_files, group_image_files


class TestFindImageFiles:
    """Tests for find_image_files function."""

    def test_finds_jpg_files(self, temp_dir):
        """Test finding JPEG files."""
        # Create test images
        (temp_dir / "image1.jpg").touch()
        (temp_dir / "image2.jpg").touch()
        (temp_dir / "other.txt").write_text("not an image")

        result = find_image_files(temp_dir)

        assert len(result) == 2
        assert all(p.suffix.lower() in [".jpg", ".jpeg"] for p in result)

    def test_finds_jpeg_files(self, temp_dir):
        """Test finding files with .jpeg extension."""
        (temp_dir / "image1.jpeg").touch()
        (temp_dir / "image2.jpeg").touch()

        result = find_image_files(temp_dir)

        assert len(result) == 2
        assert all(p.suffix.lower() == ".jpeg" for p in result)

    def test_finds_files_recursively(self, temp_dir):
        """Test finding files in subdirectories."""
        subdir = temp_dir / "subdir"
        subdir.mkdir()
        (temp_dir / "image1.jpg").touch()
        (subdir / "image2.jpg").touch()

        result = find_image_files(temp_dir)

        assert len(result) == 2

    def test_returns_empty_list_for_no_images(self, temp_dir):
        """Test returning empty list when no images found."""
        (temp_dir / "file.txt").write_text("not an image")

        result = find_image_files(temp_dir)

        assert result == []

    def test_returns_empty_list_for_empty_directory(self, temp_dir):
        """Test returning empty list for empty directory."""
        result = find_image_files(temp_dir)

        assert result == []


class TestGroupImageFiles:
    """Tests for group_image_files function."""

    def test_groups_images_by_cluster(self, temp_dir):
        """Test grouping images into cluster directories."""
        # Create test images
        img1 = temp_dir / "image1.jpg"
        img2 = temp_dir / "image2.jpg"
        img3 = temp_dir / "image3.jpg"

        Image.new("RGB", (10, 10)).save(img1, "JPEG")
        Image.new("RGB", (10, 10)).save(img2, "JPEG")
        Image.new("RGB", (10, 10)).save(img3, "JPEG")

        clustered_images = [
            ClusteredImage(path=img1, cluster_id=0),
            ClusteredImage(path=img2, cluster_id=0),
            ClusteredImage(path=img3, cluster_id=1),
        ]

        group_image_files(clustered_images, temp_dir)

        # Check that files were moved to group directories
        assert (temp_dir / "group_0" / "image1.jpg").exists()
        assert (temp_dir / "group_0" / "image2.jpg").exists()
        assert (temp_dir / "group_1" / "image3.jpg").exists()

        # Check that original files are gone
        assert not img1.exists()
        assert not img2.exists()
        assert not img3.exists()

    def test_skips_unique_images(self, temp_dir):
        """Test that unique images (cluster_id=-1) are not moved."""
        img1 = temp_dir / "image1.jpg"
        img2 = temp_dir / "image2.jpg"

        Image.new("RGB", (10, 10)).save(img1, "JPEG")
        Image.new("RGB", (10, 10)).save(img2, "JPEG")

        clustered_images = [
            ClusteredImage(path=img1, cluster_id=0),
            ClusteredImage(path=img2, cluster_id=-1),  # Unique image
        ]

        group_image_files(clustered_images, temp_dir)

        # Image1 should be moved
        assert (temp_dir / "group_0" / "image1.jpg").exists()
        assert not img1.exists()

        # Image2 should remain in place
        assert img2.exists()
        assert not (temp_dir / "group_-1").exists()

    def test_creates_output_directory(self, temp_dir):
        """Test that output directory is created if it doesn't exist."""
        output_dir = temp_dir / "output"
        img = temp_dir / "image.jpg"
        Image.new("RGB", (10, 10)).save(img, "JPEG")

        clustered_images = [ClusteredImage(path=img, cluster_id=0)]

        group_image_files(clustered_images, output_dir)

        assert output_dir.exists()
        assert (output_dir / "group_0" / "image.jpg").exists()
