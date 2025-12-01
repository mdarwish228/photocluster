# PhotoCluster

A Python package for photo clustering and organization.

## Installation

### From PyPI (when published)
```bash
pip install photocluster
```
## Usage

### Python API

The package provides a simple function-based API for clustering photos:

```python
from photocluster import photocluster

# Cluster photos with default sensitivity (0.2)
photocluster("/path/to/photos")

# Or specify a custom sensitivity
photocluster("/path/to/photos", sensitivity=0.3)
```

**Parameters:**
- `input_dir` (str | Path): Directory containing images to cluster
- `sensitivity` (float, optional): Clustering sensitivity as a proportion (0.0-1.0). Defaults to 0.2.
  - Lower values (e.g., 0.1-0.2) = stricter clustering
  - Higher values (e.g., 0.5-0.8) = looser clustering

**How it works:**
1. Scans the input directory for JPEG images (recursively)
2. Computes perceptual hashes for each image
3. Clusters similar images using DBSCAN algorithm
4. Organizes images into `group_0/`, `group_1/`, etc. subdirectories

**Example:**
```python
from pathlib import Path
from photocluster import photocluster

# Cluster photos with default sensitivity (0.2)
photocluster(Path("~/Pictures/vacation"))

# Or use a custom sensitivity for looser clustering
photocluster(Path("~/Pictures/vacation"), sensitivity=0.25)

# After running, photos will be organized like:
# ~/Pictures/vacation/
#   ├── group_0/
#   │   ├── IMG_001.jpg
#   │   └── IMG_002.jpg
#   ├── group_1/
#   │   ├── IMG_003.jpg
#   │   └── IMG_004.jpg
#   └── ...
```

## Development

### Setup development environment
```bash
git clone https://github.com/yourusername/photocluster.git
cd photocluster
uv sync --extra dev
```

### Run tests
```bash
uv run pytest
```

### Run tests with coverage
```bash
uv run pytest --cov=src/photocluster --cov-report=html
```

### Code quality checks
```bash
# Format code
uv run ruff format .

# Check code
uv run ruff check .

# Type check
uv run ty check .
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Features

- **Perceptual hashing**: Uses imagehash library to compute perceptual hashes for similarity detection
- **DBSCAN clustering**: Uses scikit-learn's DBSCAN algorithm for robust clustering
- **Multiprocessing**: Automatically uses multiple CPU cores for faster processing
- **JPEG support**: Currently supports JPEG images (.jpg, .jpeg)
- **In-place organization**: Organizes photos into cluster subdirectories within the input directory

## Changelog

### 0.1.0
- Initial release
- Basic photo clustering functionality using perceptual hashing
- Python API with `photocluster()` function
- Support for JPEG images
- Multiprocessing support for faster hash computation
