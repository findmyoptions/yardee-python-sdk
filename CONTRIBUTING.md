# Contributing to Yardee Python SDK

Thank you for your interest in contributing to the Yardee Python SDK! 🎉

## 🚀 Quick Start

1. **Fork the repository**
2. **Clone your fork**: `git clone https://github.com/yourusername/yardee-python-sdk.git`
3. **Install in development mode**: `pip install -e .`
4. **Make your changes**
5. **Submit a pull request**

## 🛠 Development Setup

```bash
# Clone the repository
git clone https://github.com/findmyoptions/yardee-python-sdk.git
cd yardee-python-sdk

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest black isort mypy

# Run tests
pytest

# Format code
black src/
isort src/
```

## 📝 Code Style

We use:
- **Black** for code formatting
- **isort** for import sorting  
- **mypy** for type checking
- **pytest** for testing

Before submitting a PR, please run:
```bash
black src/ examples/
isort src/ examples/
mypy src/
pytest
```

## 🐛 Bug Reports

When filing a bug report, please include:

- **Python version** and **OS**
- **SDK version** (`pip show yardee`)
- **Minimal code** that reproduces the issue
- **Full error traceback**
- **Expected vs actual behavior**

## ✨ Feature Requests

We love feature requests! Please include:

- **Use case** - What problem does this solve?
- **API design** - How should it work?
- **Examples** - Show expected usage

## 🔧 Types of Contributions

### 🐛 Bug Fixes
- Fix crashes, incorrect behavior, or API inconsistencies
- Improve error messages and handling
- Add missing type hints

### 📚 Documentation
- Fix typos or unclear explanations
- Add more examples
- Improve docstrings

### ✨ New Features  
- Add support for new API endpoints
- Improve developer experience
- Add utility functions

### 🧪 Tests
- Add test coverage for untested code
- Improve existing tests
- Add integration tests

## 📋 Pull Request Process

1. **Create a feature branch**: `git checkout -b feature/your-feature`
2. **Make your changes** with clear, focused commits
3. **Add tests** for new functionality
4. **Update documentation** if needed
5. **Ensure all checks pass**:
   ```bash
   black --check src/
   isort --check-only src/
   mypy src/
   pytest
   ```
6. **Submit PR** with clear description

### PR Title Format
- `feat: add support for bulk document upload`
- `fix: handle network timeouts gracefully`  
- `docs: improve search method examples`
- `test: add unit tests for client authentication`

## 🧪 Testing

We aim for high test coverage. When adding features:

- **Add unit tests** for new functions/classes
- **Add integration tests** for API interactions  
- **Test error conditions** and edge cases
- **Use meaningful test names** that describe the scenario

Example test structure:
```python
def test_search_returns_results_for_valid_query():
    client = Client(api_key="test-key")
    results = client.search(kb_id=123, query="test")
    assert len(results['results']) > 0

def test_search_raises_error_for_invalid_api_key():
    client = Client(api_key="invalid")
    with pytest.raises(AuthenticationError):
        client.search(kb_id=123, query="test")
```

## 📋 Code Review Checklist

Before submitting, ensure:

- [ ] Code follows project style (Black + isort)
- [ ] Type hints are added for new functions
- [ ] Tests are added for new functionality
- [ ] Documentation is updated if needed
- [ ] Error handling is appropriate
- [ ] No breaking changes (or clearly documented)

## 🌟 Recognition

Contributors will be:
- **Listed in CONTRIBUTORS.md**
- **Mentioned in release notes**
- **Credited in documentation**

## 📞 Getting Help

- **Email**: [support@yardee.ai](mailto:support@yardee.ai)

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make Yardee better! 🚀