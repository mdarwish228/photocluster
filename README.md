# PhotoCluster

A Python package for photo clustering and organization.

## Installation

### From PyPI (when published)
```bash
pip install photocluster
```

### From source
```bash
git clone https://github.com/yourusername/photocluster.git
cd photocluster
pip install -e .
```

### Using UV
```bash
uv add photocluster
```

## Usage

### Command Line Interface

#### Cluster photos
```bash
photocluster cluster /path/to/photos
```

#### Organize photos
```bash
photocluster organize /path/to/source /path/to/target
```

### Python API

```python
from photocluster import PhotoCluster

# Create a PhotoCluster instance
clusterer = PhotoCluster()

# Cluster photos in a directory
clusterer.cluster_photos("/path/to/photos")

# Organize photos from source to target directory
clusterer.organize_photos("/path/to/source", "/path/to/target")
```

## Development

### Setup development environment
```bash
git clone https://github.com/yourusername/photocluster.git
cd photocluster
uv sync --dev
```

### Run tests
```bash
uv run pytest
```

### Build package
```bash
uv build
```

### Publish to PyPI
```bash
# Build the package
uv build

# Publish to PyPI (you'll need PyPI credentials)
uv publish

# Or publish to PyPI Test first (recommended)
uv publish --index-url https://test.pypi.org/simple/
```

## Publishing to PyPI

### Prerequisites
1. **Update personal information** in `pyproject.toml`:
   - Replace "Your Name" with your actual name
   - Replace "your.email@example.com" with your email
   - Update GitHub URLs with your actual repository

2. **Set up PyPI credentials**:
   - Create an API token at https://pypi.org/manage/account/token/
   - Configure authentication (uv will prompt for credentials when needed)

### Publishing Steps
1. **Build the package**:
   ```bash
   uv build
   ```

2. **Test locally** (optional):
   ```bash
   # Install the built package locally
   pip install dist/photocluster-0.1.0-py3-none-any.whl
   
   # Test the CLI
   photocluster --help
   ```

3. **Publish to PyPI Test first** (recommended):
   ```bash
   uv publish --index-url https://test.pypi.org/simple/
   ```

4. **Publish to PyPI**:
   ```bash
   uv publish
   ```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### 0.1.0
- Initial release
- Basic photo clustering functionality
- Command-line interface
- Python API
