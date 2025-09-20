# PyPI Publishing Guide

## Prerequisites
1. PyPI account with 2FA enabled
2. API token created

## Publishing Steps

### 1. Set up credentials
```bash
# Option A: Using keyring (recommended)
python3.11 -m keyring set https://upload.pypi.org/legacy/ __token__

# Option B: Create ~/.pypirc file
cat > ~/.pypirc << EOF
[pypi]
username = __token__
password = pypi-your-api-token-here
EOF
```

### 2. Upload to PyPI
```bash
cd /Users/aa/Documents/Coding/Yardee/yardee_sdk
python3.11 -m twine upload dist/*
```

### 3. Verify Installation
```bash
pip install yardee
```

## Future Updates
1. Update version in `pyproject.toml`
2. Create new git tag: `git tag v0.1.1 && git push origin v0.1.1`
3. Build: `python3.11 -m build`
4. Upload: `python3.11 -m twine upload dist/*`

## Test PyPI (Optional)
```bash
# Upload to test PyPI first
python3.11 -m twine upload --repository testpypi dist/*

# Install from test PyPI
pip install --index-url https://test.pypi.org/simple/ yardee
```