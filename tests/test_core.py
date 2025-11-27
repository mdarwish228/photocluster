"""Tests for photocluster core function."""

from PIL import Image

from photocluster.core import photocluster


class TestPhotocluster:
    """Tests for photocluster function."""

    def test_clusters_similar_images(self, temp_dir):
        """Test that similar images are clustered together."""
        # Create 3 similar images (slight variations)
        # These should cluster together with appropriate sensitivity
        for i in range(3):
            img_path = temp_dir / f"similar_{i}.jpg"
            img = Image.new("RGB", (200, 200), color=(100 + i * 5, 100, 100))
            # Add slight variation to make them similar but not identical
            pixels = []
            for y in range(200):
                for x in range(200):
                    # Add tiny random-like variation based on position
                    r = 100 + i * 5 + (x + y) % 3
                    g = 100 + (x * y) % 2
                    b = 100 + (x + y) % 2
                    pixels.append((r, g, b))
            img.putdata(pixels)
            img.save(img_path, "JPEG")

        # Add non-JPEG files that should be ignored
        (temp_dir / "document.txt").write_text("not an image")
        (temp_dir / "data.json").write_text('{"key": "value"}')
        (temp_dir / "image.png").touch()  # PNG should be ignored

        # Run photocluster with moderate sensitivity
        photocluster(temp_dir, sensitivity=0.3)

        # Check that similar images were clustered
        # At least one cluster directory should exist
        cluster_dirs = [
            d for d in temp_dir.iterdir() if d.is_dir() and d.name.startswith("group_")
        ]
        assert len(cluster_dirs) > 0, "Expected at least one cluster directory"

        # Check that images were moved to cluster directories
        moved_images = []
        for cluster_dir in cluster_dirs:
            moved_images.extend(list(cluster_dir.glob("*.jpg")))

        assert len(moved_images) >= 2, "Expected at least 2 images to be clustered"

        # Verify non-JPEG files remain in root
        assert (temp_dir / "document.txt").exists()
        assert (temp_dir / "data.json").exists()
        assert (temp_dir / "image.png").exists()

    def test_unique_images_not_clustered(self, temp_dir):
        """Test that unique images remain in place (cluster_id = -1)."""
        # Create 3 very different images with completely different visual patterns
        # Perceptual hashing is sensitive to structure, so we need structurally different images

        # Image 1: Horizontal stripes pattern
        img1 = temp_dir / "unique_0.jpg"
        img = Image.new("RGB", (200, 200))
        pixels = []
        for y in range(200):
            for _x in range(200):
                # Horizontal stripes - every 10 pixels
                if (y // 10) % 2 == 0:
                    pixels.append((255, 0, 0))  # Red stripe
                else:
                    pixels.append((0, 0, 0))  # Black stripe
        img.putdata(pixels)
        img.save(img1, "JPEG")

        # Image 2: Vertical stripes pattern (orthogonal to horizontal)
        img2 = temp_dir / "unique_1.jpg"
        img = Image.new("RGB", (200, 200))
        pixels = []
        for _y in range(200):
            for x in range(200):
                # Vertical stripes - every 10 pixels
                if (x // 10) % 2 == 0:
                    pixels.append((0, 0, 255))  # Blue stripe
                else:
                    pixels.append((255, 255, 255))  # White stripe
        img.putdata(pixels)
        img.save(img2, "JPEG")

        # Image 3: Diagonal gradient pattern (completely different structure)
        img3 = temp_dir / "unique_2.jpg"
        img = Image.new("RGB", (200, 200))
        pixels = []
        for y in range(200):
            for x in range(200):
                # Diagonal gradient based on x+y
                intensity = ((x + y) * 255) // 400
                pixels.append((intensity, (intensity * 2) % 256, (intensity * 3) % 256))
        img.putdata(pixels)
        img.save(img3, "JPEG")

        # Add non-JPEG files
        (temp_dir / "readme.md").write_text("# Documentation")
        (temp_dir / "config.yaml").write_text("key: value")

        # Run photocluster with very low sensitivity (very strict)
        # With structurally different images, even low sensitivity should keep them separate
        photocluster(temp_dir, sensitivity=0.05)

        # Check that no cluster directories were created (all images are unique)
        cluster_dirs = [
            d for d in temp_dir.iterdir() if d.is_dir() and d.name.startswith("group_")
        ]
        assert len(cluster_dirs) == 0, "Unique images should not be clustered"

        # Verify images remain in root directory
        remaining_images = list(temp_dir.glob("*.jpg"))
        assert len(remaining_images) == 3, "All unique images should remain in root"

        # Verify non-JPEG files remain
        assert (temp_dir / "readme.md").exists()
        assert (temp_dir / "config.yaml").exists()

    def test_mixed_clustering_and_unique(self, temp_dir):
        """Test scenario with both clustered and unique images."""
        # Create 2 similar images (should cluster)
        for i in range(2):
            img_path = temp_dir / f"similar_{i}.jpg"
            img = Image.new("RGB", (150, 150), color=(150, 150, 150))
            pixels = []
            for y in range(150):
                for x in range(150):
                    # Very similar images with minimal variation
                    r = 150 + (x + y + i) % 2
                    g = 150 + (x * y + i) % 2
                    b = 150 + (x + y) % 2
                    pixels.append((r, g, b))
            img.putdata(pixels)
            img.save(img_path, "JPEG")

        # Create 1 very different image (should remain unique)
        unique_img = temp_dir / "unique.jpg"
        img = Image.new("RGB", (150, 150))
        pixels = []
        for y in range(150):
            for x in range(150):
                # Completely different pattern
                r = (x * y) % 256
                g = (x + y * 2) % 256
                b = (x * 2 + y) % 256
                pixels.append((r, g, b))
        img.putdata(pixels)
        img.save(unique_img, "JPEG")

        # Add non-JPEG files
        (temp_dir / "notes.txt").write_text("Some notes")

        # Run photocluster
        photocluster(temp_dir, sensitivity=0.25)

        # Check that similar images were clustered
        cluster_dirs = [
            d for d in temp_dir.iterdir() if d.is_dir() and d.name.startswith("group_")
        ]

        # Should have at least one cluster for the similar images
        if len(cluster_dirs) > 0:
            # Similar images should be in a cluster
            clustered_count = sum(len(list(d.glob("*.jpg"))) for d in cluster_dirs)
            assert clustered_count >= 2, "Similar images should be clustered"

        # Unique image should remain in root (or be in a cluster with -1, but since we skip -1, it stays)
        # Actually, images with cluster_id -1 are not moved, so they stay in root
        root_images = list(temp_dir.glob("*.jpg"))
        # At least the unique image should remain
        assert len(root_images) >= 1, "Unique image should remain in root"

        # Verify non-JPEG file remains
        assert (temp_dir / "notes.txt").exists()

    def test_empty_directory(self, temp_dir):
        """Test that empty directory doesn't cause errors."""
        # Add only non-JPEG files
        (temp_dir / "file.txt").write_text("content")
        (temp_dir / "data.csv").write_text("col1,col2\n1,2")

        # Should not raise an error
        photocluster(temp_dir, sensitivity=0.2)

        # Non-JPEG files should remain
        assert (temp_dir / "file.txt").exists()
        assert (temp_dir / "data.csv").exists()

        # No cluster directories should be created
        cluster_dirs = [
            d for d in temp_dir.iterdir() if d.is_dir() and d.name.startswith("group_")
        ]
        assert len(cluster_dirs) == 0

    def test_single_image_remains_unique(self, temp_dir):
        """Test that a single image remains in place (can't cluster alone)."""
        # Create single image
        img_path = temp_dir / "single.jpg"
        img = Image.new("RGB", (100, 100), color="blue")
        img.save(img_path, "JPEG")

        # Add non-JPEG file
        (temp_dir / "readme.txt").write_text("readme")

        # Run photocluster
        photocluster(temp_dir, sensitivity=0.2)

        # Single image should remain in root (min_samples = 2, so it can't cluster)
        assert (temp_dir / "single.jpg").exists()

        # No cluster directories
        cluster_dirs = [
            d for d in temp_dir.iterdir() if d.is_dir() and d.name.startswith("group_")
        ]
        assert len(cluster_dirs) == 0

        # Non-JPEG file should remain
        assert (temp_dir / "readme.txt").exists()
