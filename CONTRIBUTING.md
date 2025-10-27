# Contributing to Document Search API

Thank you for your interest in contributing to the Document Search API! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your environment (OS, Python version, etc.)
- Any relevant logs or error messages

### Suggesting Enhancements

We welcome feature requests! Please open an issue with:
- A clear description of the enhancement
- Use cases and benefits
- Any implementation ideas (optional)

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following the code style of the project
3. **Add tests** if applicable
4. **Update documentation** if needed
5. **Ensure all tests pass**
6. **Submit a pull request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/EmbeddingSearch.git
cd EmbeddingSearch

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_api.py
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions focused and modular

### Testing

- Test your changes thoroughly
- Add unit tests for new features
- Ensure existing tests still pass

### Commit Messages

- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, etc.)
- Reference issues when applicable

Example:
```
Add batch upload support for multiple PDFs (#42)
Fix search relevance scoring for short queries (#38)
Update documentation for Docker deployment
```

## Code of Conduct

Be respectful and constructive in all interactions. We aim to maintain a welcoming and inclusive community.

## Questions?

Feel free to open an issue for any questions or clarifications.

Thank you for contributing! 🎉
