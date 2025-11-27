"""Processing utilities for PhotoCluster."""

import multiprocessing

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
    return max(MIN_PROCESSES, min(MAX_PROCESSES, int(cpu_count * CPU_USAGE_RATIO)))
