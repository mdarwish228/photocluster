"""Tests for validation models."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from photocluster.internal.models.validation import PhotoclusterInputs


class TestPhotoclusterInputs:
    """Tests for PhotoclusterInputs validation."""

    def test_valid_inputs(self, temp_dir):
        """Test validation with valid inputs."""
        inputs = PhotoclusterInputs(input_dir=temp_dir, sensitivity=0.2)

        assert inputs.input_dir == Path(temp_dir)
        assert inputs.sensitivity == 0.2

    def test_sensitivity_min_value(self, temp_dir):
        """Test sensitivity at minimum value (0.0)."""
        inputs = PhotoclusterInputs(input_dir=temp_dir, sensitivity=0.0)

        assert inputs.sensitivity == 0.0

    def test_sensitivity_max_value(self, temp_dir):
        """Test sensitivity at maximum value (1.0)."""
        inputs = PhotoclusterInputs(input_dir=temp_dir, sensitivity=1.0)

        assert inputs.sensitivity == 1.0

    def test_sensitivity_below_minimum(self, temp_dir):
        """Test validation error for sensitivity below 0.0."""
        with pytest.raises(ValidationError):
            PhotoclusterInputs(input_dir=temp_dir, sensitivity=-0.1)

    def test_sensitivity_above_maximum(self, temp_dir):
        """Test validation error for sensitivity above 1.0."""
        with pytest.raises(ValidationError):
            PhotoclusterInputs(input_dir=temp_dir, sensitivity=1.1)

    def test_nonexistent_directory(self):
        """Test validation error for nonexistent directory."""
        with pytest.raises(ValidationError):
            PhotoclusterInputs(
                input_dir=Path("/nonexistent/path/12345"), sensitivity=0.2
            )

    def test_file_instead_of_directory(self, temp_dir):
        """Test validation error when path is a file, not directory."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test")

        with pytest.raises(ValidationError):
            PhotoclusterInputs(input_dir=test_file, sensitivity=0.2)
