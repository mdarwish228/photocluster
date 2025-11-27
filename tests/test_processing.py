"""Tests for processing utilities."""

from unittest.mock import patch

from photocluster.internal.util.processing import (
    CPU_USAGE_RATIO,
    MAX_PROCESSES,
    MIN_PROCESSES,
    get_num_processes,
)


class TestGetNumProcesses:
    """Tests for get_num_processes function."""

    def test_returns_integer(self):
        """Test that get_num_processes returns an integer."""
        result = get_num_processes()
        assert isinstance(result, int)

    def test_respects_minimum(self):
        """Test that result is at least MIN_PROCESSES."""
        result = get_num_processes()
        assert result >= MIN_PROCESSES

    def test_respects_maximum(self):
        """Test that result is at most MAX_PROCESSES."""
        result = get_num_processes()
        assert result <= MAX_PROCESSES

    @patch("multiprocessing.cpu_count")
    def test_calculation_with_low_cpu_count(self, mock_cpu_count):
        """Test calculation with low CPU count."""
        mock_cpu_count.return_value = 1
        result = get_num_processes()
        assert result == MIN_PROCESSES

    @patch("multiprocessing.cpu_count")
    def test_calculation_with_high_cpu_count(self, mock_cpu_count):
        """Test calculation with high CPU count."""
        mock_cpu_count.return_value = 20
        result = get_num_processes()
        # Should be min(MAX_PROCESSES, int(20 * CPU_USAGE_RATIO))
        expected = min(MAX_PROCESSES, int(20 * CPU_USAGE_RATIO))
        assert result == expected

    @patch("multiprocessing.cpu_count")
    def test_calculation_with_medium_cpu_count(self, mock_cpu_count):
        """Test calculation with medium CPU count."""
        mock_cpu_count.return_value = 4
        result = get_num_processes()
        expected = max(MIN_PROCESSES, min(MAX_PROCESSES, int(4 * CPU_USAGE_RATIO)))
        assert result == expected
