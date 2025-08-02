
<!-- Optional: Add your project logo/banner here -->
<!-- ![Project Logo](docs/logo.png) -->

# Python Project Template

[![CI](https://github.com/mberetvas/python-template/actions/workflows/ci-python.yml/badge.svg)](https://github.com/mberetvas/python-template/actions/workflows/ci-python.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> A modern, opinionated Python template for slick, no-nonsense development. Get started fast, keep your code clean, and let the tools do the heavy lifting. Built for devs who want less faff and more results.


## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Development](#development)
  - [Running the Application](#running-the-application)
  - [Running Tests](#running-tests)
  - [Code Quality](#code-quality)
  - [Configuring Ruff](#configuring-ruff)
- [AI-Powered Development](#ai-powered-development)
  - [GitHub Copilot Integration](#github-copilot-integration)
  - [Using Custom Prompts](#using-custom-prompts)
  - [Available Prompts](#available-prompts)
- [Instructions & Chat Modes](#instructions--chat-modes)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Support](#support)
- [License](#license)


## Features

- **Modern Tooling**: Uses [`uv`](https://github.com/astral-sh/uv) for lightning-fast package management.
- **Organized Structure**: Source in [`src/`](src/), tests in [`tests/`](tests/), config in [`Ruff-config/`](Ruff-config/).
- **Testing Ready**: [`pytest`](https://docs.pytest.org/) with JUnit XML output for CI/CD.
- **Code Quality**: [`ruff`](https://docs.astral.sh/ruff/) for linting/formatting, pre-configured for PEP 8.
- **CI/CD Ready**: GitHub Actions workflow out of the box.
- **Version Control**: Robust `.gitignore` for Python projects.
- **VS Code Integration**: Workspace settings and [Ruff extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff) for a smooth dev experience.
- **AI-Powered Development**: Custom Copilot prompts for code, tests, and reviews in [`.github/prompts/`](.github/prompts/).
- **Pull Request Templates**: Consistent PRs with [`.github/pull_request_template.md`](.github/pull_request_template.md).


## Quick Start

Want to get going faster than a rat up a drainpipe? Here’s the bare minimum:

```sh
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY-NAME.git
cd YOUR-REPOSITORY-NAME
uv init && uv venv
.venv\Scripts\activate  # On Windows
uv add -r requirements.txt
python src/main.py
```

## Getting Started

Step-by-step for the cautious types:



### Prerequisites

Before you get your hands dirty, make sure you’ve got the right tools:

- [uv](https://github.com/astral-sh/uv) – Handles your Python environments and packages faster than a whippet on Red Bull.
- [Python 3.9+](https://www.python.org/downloads/) – None of that ancient Python 2 rubbish.

Want to check if `uv` is already lurking on your system? Run this:
```sh
uv --version
```
If your terminal throws a wobbly and says it’s not found, just slap this in:
```sh
pip install uv
```
That’s it. No faffing about.


### Installation

Right, let’s get this show on the road. Follow these steps and you’ll be up and running before you can say “pip is slow”.

1.  **Create your own copy of this template.**
    Hit the “Use this template” button on GitHub. Don’t be shy.

2.  **Clone your shiny new repo.**
    ```sh
    git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY-NAME.git
    cd YOUR-REPOSITORY-NAME
    ```

3.  **Set up your virtual environment.**
    This keeps your dependencies tidier than a nun’s sock drawer.
    ```sh
    uv init
    uv venv
    ```
    Activate it:
    - On macOS/Linux: `source .venv/bin/activate`
    - On Windows: `.venv\Scripts\activate`

4.  **Install your dependencies.**
    Get your project’s packages sorted:
    ```sh
    uv add -r requirements.txt
    ```
    *(If you haven’t got a `requirements.txt` yet, make one. Don’t be a muppet.)*

## Development

### Running the Application

To run the example entry point when the venv has been activated:
```sh
python src/main.py
```
If the the venv is not activated use:
```sh
uv run src/main.py
```

### Running Tests

This template uses `pytest` for testing with JUnit XML output for CI/CD integration.

```sh
# Install pytest if you haven't already
uv add --dev pytest

# Run tests with JUnit XML output
pytest --junitxml=junit/test-results.xml

# Run tests (simple)
pytest
```

The test results are automatically saved to `junit/test-results.xml` for integration with CI/CD systems.

### Code Quality

 [VS Code](https://docs.astral.sh/ruff/editors/setup/#vs-code)

Install the Ruff extension from the [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff). It is recommended to have the Ruff extension version `2024.32.0` or later to get the best experience with the Ruff Language Server.

For more documentation on the Ruff extension, refer to the [README](https://github.com/astral-sh/ruff-vscode/blob/main/README.md) of the extension repository.

Or by simply using the ruff tool:

This template uses `ruff` for linting and formatting.
```sh
# Install Ruff globally.
uv tool install ruff@latest

# Once installed, you can run Ruff from the command line:

ruff check   # Lint all files in the current directory.
ruff format  # Format all files in the current directory.
```

### Configuring Ruff

Ruff's behavior is controlled by the `Ruff-config/ruff.toml` file. This template comes with a pre-configured file that sets sensible defaults for the project, including:

-   **Excluding common directories** from linting and formatting.
-   **Setting the line-length** to 100 characters.
-   **Targeting Python 3.9** for compatibility.
-   **Enabling a standard set of rules** for code quality.

You can customize the linting and formatting rules by editing this file. For a complete list of options, see the [official Ruff documentation](https://docs.astral.sh/ruff/configuration/).

## AI-Powered Development

This template includes a comprehensive collection of GitHub Copilot prompts designed to accelerate your Python development workflow. These prompts are located in the `.github/prompts/` directory and are automatically recognized by VS Code with GitHub Copilot.

### GitHub Copilot Integration

The project is pre-configured to work seamlessly with GitHub Copilot through VS Code settings:

- **Prompt Files**: Custom prompts are automatically detected from `.github/prompts/`
- **Chat Modes**: AI-powered development assistance
- **Instructions**: Context-aware coding guidelines

### Using Custom Prompts

To use the included prompts:

1. **Open VS Code** with the GitHub Copilot extension installed
2. **Select code** you want to work with
3. **Open GitHub Copilot Chat** (Ctrl+Shift+I / Cmd+Shift+I)
4. **Type `@workspace`** followed by the prompt name (e.g., `@workspace /write-pytest`)
5. **Execute the prompt** to generate code, tests, or reviews

### Available Prompts

The template includes the following ready-to-use prompts:

#### Code Generation
- **`asyncify-io.prompt.md`** - Convert synchronous I/O operations to async/await
- **`create-class.prompt.md`** - Generate Python classes with proper structure
- **`extract-function.prompt.md`** - Extract reusable functions from code blocks
- **`generate-dataclass.prompt.md`** - Create Python dataclasses with type hints
- **`generate-new-cli.prompt.md`** - Generate complete CLI applications
- **`quick-cli.prompt.md`** - Convert code selections into CLI scripts

#### Testing & Documentation
- **`docstringify.prompt.md`** - Generate comprehensive docstrings
- **`generate-pytest-tests.prompt.md`** - Create comprehensive test suites
- **`write-pytest.prompt.md`** - Generate pytest cases for selected code

#### Code Review & Quality
- **`lightweight-review.prompt.md`** - Quick code quality assessment
- **`review-code-general.prompt.md`** - Comprehensive code review
- **`review-code-performance.prompt.md`** - Performance-focused code analysis
- **`security-review.prompt.md`** - Security-centric code review

#### Refactoring & Optimization
- **`optimize-loop.prompt.md`** - Optimize loop performance
- **`refactor-add-error-handling.prompt.md`** - Add robust error handling
- **`refactor-readability.prompt.md`** - Improve code readability

#### Utilities
- **`explain-code-block.md`** - Get detailed code explanations

Each prompt is designed to work with code selections and provides context-aware suggestions following Python best practices.

## Instructions & Chat Modes

**Instructions files** (in `.github/instructions/`) define coding standards, best practices, or project-specific rules for GitHub Copilot and compatible tools. When present, these files guide Copilot to generate, review, and refactor code according to your team's requirements. For example, an instructions file can enforce PEP 8, require type hints, or specify how to handle edge cases in Python code.

**Chatmodes files** (in `.github/chatmodes/`) define custom behaviors or workflows for Copilot Chat. Each chatmode can change how Copilot responds in chat, such as acting as a code reviewer, pair programmer, or security auditor. By switching chatmodes, you can tailor Copilot's responses to different development scenarios or team roles.

Both instructions and chatmodes are automatically detected by VS Code and Copilot if present, and can be referenced in Copilot Chat using the `@workspace` command, just like prompts.

**Example usage:**
- `@workspace /instructions/python-coding-conventions` — Apply your custom Python coding rules
- `@workspace /chatmodes/ai-reviewer` — Switch to a custom AI reviewer chat mode

> Add your own files to `.github/instructions/` and `.github/chatmodes/` to further customize Copilot's behavior for your project.

### Files in `.github/instructions/`
- **python-codegeneration.instructions.md** — Python coding conventions and guidelines: Enforces PEP 8, type hints, docstrings, and best practices for Python code generation.
- **testgeneration.instructions.md** — Guidelines for generating pytest unit & integration tests: Specifies naming, structure, fixtures, and parametrization for tests.
- **reviewSelection.instructions.md** — Standard code review checklist for Python projects: Provides a structured peer review process with actionable, friendly feedback.
- **copilot-commit-message-instructions.md** — Commit message guidelines: Enforces Conventional Commits format with gitmoji and clear, informative commit messages.

### Files in `.github/chatmodes/`
- **refine-issue.chatmode.md** — Refine requirements or issues: Adds acceptance criteria, technical considerations, edge cases, and NFRs to GitHub issues.
- **prd.chatmode.md** — Product Requirements Document (PRD) mode: Generates comprehensive PRDs in Markdown, including user stories and acceptance criteria.
- **planner.chatmode.md** — Planning mode: Generates implementation plans for new features or refactoring, including requirements and testing steps.
- **markdown-master.chatmode.md** — Markdown content standards: Enforces documentation and content creation rules for Markdown files.
- **explainer.chatmode.md** — Explainer mode: Systematically explains code with context, structure, and clarity for developers.
- **debug.chatmode.md** — Debug mode: Guides users through a structured debugging process to identify and resolve bugs.
- **database.chatmode.md** — Database administrator mode: Assists with managing, querying, and optimizing relational databases.
- **4.1-Beast.chatmode.md** — GPT-4.1 Coding Agent: A system prompt for a top-notch coding agent that manages tasks, todo lists, and problem resolution.

> Add or customize files in these folders to further tailor Copilot's behavior for your team or project.

## Project Structure

```
python-template/
├── .github/
│   ├── prompts/               # AI-powered development prompts
│   │   ├── asyncify-io.prompt.md
│   │   ├── create-class.prompt.md
│   │   ├── docstringify.prompt.md
│   │   ├── explain-code-block.md
│   │   ├── extract-function.prompt.md
│   │   ├── generate-dataclass.prompt.md
│   │   ├── generate-new-cli.prompt.md
│   │   ├── generate-pytest-tests.prompt.md
│   │   ├── lightweight-review.prompt.md
│   │   ├── optimize-loop.prompt.md
│   │   ├── quick-cli.prompt.md
│   │   ├── refactor-add-error-handling.prompt.md
│   │   ├── refactor-readability.prompt.md
│   │   ├── review-code-general.prompt.md
│   │   ├── review-code-performance.prompt.md
│   │   ├── security-review.prompt.md
│   │   └── write-pytest.prompt.md
│   ├── workflows/
│   │   └── ci-python.yml      # GitHub Actions CI/CD workflow
│   └── pull_request_template.md
├── .vscode/
│   └── settings.json          # VS Code workspace settings
├── junit/
│   └── test-results.xml       # JUnit test results (generated)
├── Ruff-config/
│   └── ruff.toml             # Ruff linting and formatting configuration
├── src/
│   ├── __init__.py
│   └── main.py               # Main application entry point
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # pytest configuration
│   └── tests.py              # Test cases
├── .gitignore                # Git ignore rules
├── LICENSE                   # MIT License
├── README.md                 # This file
└── requirements.txt          # Python dependencies
```

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
