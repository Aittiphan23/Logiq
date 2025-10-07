# Contributing to Logiq

Thank you for considering contributing to Logiq! 🎉

## 📋 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the issue, not the person
- Help others learn and grow

## 🚀 How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported
2. Use the bug report template
3. Include reproduction steps
4. Provide system information
5. Add relevant logs/screenshots

### Suggesting Features

1. Check if feature already exists or is planned
2. Use the feature request template
3. Explain the use case
4. Provide examples
5. Consider implementation details

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
   - Follow code style guidelines
   - Add/update tests
   - Update documentation
4. **Test your changes**
   ```bash
   pytest
   ```
5. **Commit your changes**
   ```bash
   git commit -m "feat: add amazing feature"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

## 📝 Code Style

### Python

- Follow PEP 8
- Use type hints
- Add docstrings
- Keep functions focused
- Maximum line length: 100 characters

### Example

```python
async def create_user(self, user_id: int, guild_id: int) -> Dict[str, Any]:
    """
    Create a new user in the database

    Args:
        user_id: Discord user ID
        guild_id: Discord guild ID

    Returns:
        User document dictionary
    """
    user_data = {
        "user_id": user_id,
        "guild_id": guild_id,
        "xp": 0
    }
    await self.db.users.insert_one(user_data)
    return user_data
```

## 🧪 Testing

- Write tests for new features
- Ensure all tests pass
- Aim for >80% code coverage

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html
```

## 📚 Documentation

- Update README.md for new features
- Add docstrings to functions
- Update DEPLOYMENT.md if needed
- Include examples

## 🏷️ Commit Messages

Use conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test changes
- `chore:` Build/config changes

Examples:
- `feat: add economy system`
- `fix: resolve database connection issue`
- `docs: update installation guide`

## 🔍 Code Review Process

1. Automated checks run on PR
2. Maintainer reviews code
3. Feedback provided
4. Changes requested if needed
5. Approval and merge

## 🎯 Areas for Contribution

- 🐛 Bug fixes
- ✨ New features
- 📝 Documentation
- 🧪 Tests
- 🎨 UI/UX improvements
- 🌍 Translations
- ⚡ Performance optimizations

## ❓ Questions?

- Open an issue
- Join our Discord
- Check existing documentation

Thank you for contributing! 🙏
