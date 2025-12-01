"""Processing utilities for PhotoCluster."""

import logging
import multiprocessing

logger = logging.getLogger(__name__)

MIN_PROCESSES = 1
MAX_PROCESSES = 8
CPU_USAGE_RATIO = 0.75


def get_num_processes() -> int:
    """Calculate the default number of processes to use for parallel processing.

    Uses 75% of available CPU cores, with a minimum of 1 and maximum of 8.

    Returns:
        Number of processes to use
    """
    cpu_count = multiprocessing.cpu_count()
    num_processes = max(
        MIN_PROCESSES, min(MAX_PROCESSES, int(cpu_count * CPU_USAGE_RATIO))
    )
    logger.debug(f"Detected {cpu_count} CPU cores, using {num_processes} processes")
    return num_processes
