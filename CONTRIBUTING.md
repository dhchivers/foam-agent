# Contributing to FoamAgent

We welcome contributions to FoamAgent! This document provides guidelines for contributing.

## Development Setup

### Prerequisites

- Docker Engine 20.10+
- Git
- Basic knowledge of Qt6 and C++
- Familiarity with OpenFOAM (helpful but not required)

### Setting Up Development Environment

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd FoamAgent
   ```

2. Build the Docker container:
   ```bash
   ./scripts/build.sh
   ```

3. Run in development mode:
   ```bash
   ./scripts/dev.sh
   ```

## Project Structure

```
FoamAgent/
├── src/              # C++ source files
├── ui/               # Qt Designer UI files
├── docker/           # Docker configuration
├── scripts/          # Build and run scripts
├── examples/         # Example case templates
└── tests/            # Unit tests (to be added)
```

## Coding Standards

### C++ Code

- Follow Qt coding conventions
- Use meaningful variable and function names
- Add comments for complex logic
- Use Qt classes (QString, QList, etc.) instead of STL where appropriate
- Keep functions focused and small

### Code Style

```cpp
// Class names: PascalCase
class MeshWidget : public QWidget
{
    // Member variables: camelCase with m_ prefix
    CaseManager *m_caseManager;
    
    // Methods: camelCase
    void runBlockMesh();
};
```

### Commits

- Write clear, concise commit messages
- Use present tense ("Add feature" not "Added feature")
- Reference issue numbers when applicable
- Keep commits focused on a single change

Example:
```
Add mesh quality checking feature

- Implement checkMesh command execution
- Add quality metrics display
- Update UI with quality indicators

Fixes #123
```

## Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Pull Request Guidelines

- Provide a clear description of the changes
- Include screenshots for UI changes
- Ensure all tests pass (when test suite is available)
- Update documentation as needed
- Keep PRs focused on a single feature or fix

## Testing

Currently, testing should be done manually:

1. Build the container
2. Run the application
3. Test all affected features
4. Verify no regressions in existing functionality

We plan to add automated testing in the future.

## Adding New Features

When adding new features:

1. **Plan**: Discuss major features in an issue first
2. **Implement**: Follow existing patterns and conventions
3. **Document**: Update README and add inline comments
4. **Test**: Verify the feature works as expected
5. **Examples**: Add templates or examples if applicable

## Reporting Bugs

Use GitHub Issues to report bugs. Include:

- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Docker version)
- Screenshots or logs if applicable

## Feature Requests

We welcome feature requests! Please:

- Check existing issues first
- Provide clear use case and motivation
- Describe expected behavior
- Be open to discussion and alternatives

## Questions?

Feel free to open an issue for questions or join our discussions.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
