# Gemini CLI Setup and Management

This skill provides comprehensive guidance for installing, executing, and managing releases of Gemini CLI, Google's AI-powered coding assistant. It covers system requirements, multiple installation methods, execution options, and release channels to ensure you can get Gemini CLI running in your environment.

## Recommended System Specifications

- **Operating System:**
  - macOS 15+
  - Windows 11 24H2+
  - Ubuntu 20.04+
- **Hardware:**
  - "Casual" usage: 4GB+ RAM (short sessions, common tasks and edits)
  - "Power" usage: 16GB+ RAM (long sessions, large codebases, deep context)
- **Runtime:** Node.js 20.0.0+
- **Shell:** Bash, Zsh, or PowerShell
- **Location:** [Gemini Code Assist supported locations](https://developers.google.com/gemini-code-assist/resources/available-locations#americas)
- **Internet connection required**

## Installation Methods

Gemini CLI can be installed using several methods. Choose the one that best fits your environment:

### npm (Recommended for most users)

Install globally with npm:

```bash
npm install -g @google/gemini-cli
```

### Homebrew (macOS/Linux)

Install globally with Homebrew:

```bash
brew install gemini-cli
```

### MacPorts (macOS)

Install globally with MacPorts:

```bash
sudo port install gemini-cli
```

### Anaconda (for restricted environments)

Install with Anaconda:

```bash
# Create and activate a new environment
conda create -y -n gemini_env -c conda-forge nodejs
conda activate gemini_env

# Install Gemini CLI globally via npm (inside the environment)
npm install -g @google/gemini-cli
```

Note: Gemini CLI comes pre-installed on [Cloud Shell](https://docs.cloud.google.com/shell/docs) and [Cloud Workstations](https://cloud.google.com/workstations).

## Execution Options

### Basic Execution

For most users, run Gemini CLI with the `gemini` command:

```bash
gemini
```

For a list of options and additional commands, see the [CLI cheatsheet](/docs/cli/cli-reference).

### Advanced Execution Methods

#### npx (No Installation Required)

Run instantly with npx:

```bash
npx @google/gemini-cli
```

Execute directly from GitHub main branch (for testing development features):

```bash
npx https://github.com/google-gemini/gemini-cli
```

#### Docker/Podman Sandbox (for security and isolation)

Run the published sandbox image directly:

```bash
docker run --rm -it us-docker.pkg.dev/gemini-code-dev/gemini-cli/sandbox:0.1.1
```

Or use the `--sandbox` flag with local installation:

```bash
gemini --sandbox -y -p "your prompt here"
```

#### From Source (for contributors)

Development mode with hot-reloading:

```bash
# From the root of the repository
npm run start
```

Production mode with React optimizations:

```bash
# From the root of the repository
npm run start:prod
```

Production-like mode with linked package:

```bash
# Link the local cli package to your global node_modules
npm link packages/cli

# Now you can run your local version using the `gemini` command
gemini
```

## Release Channels

Gemini CLI has three release channels:

### Stable (Recommended)

Weekly stable releases from the previous week's preview plus bug fixes. Uses `latest` tag:

```bash
npm install -g @google/gemini-cli
npm install -g @google/gemini-cli@latest
```

### Preview

Weekly preview releases (may contain regressions):

```bash
npm install -g @google/gemini-cli@preview
```

### Nightly

Daily releases from main branch (untested changes):

```bash
npm install -g @google/gemini-cli@nightly
```

## Troubleshooting

- Ensure Node.js 20.0.0+ is installed
- Check internet connectivity for Gemini Code Assist locations
- For Docker execution, ensure Docker/Podman is running
- Verify shell compatibility (Bash, Zsh, PowerShell)

## Integration with OSINT Workflows

While Gemini CLI is primarily a coding assistant, it can be integrated into OSINT (Open Source Intelligence) projects for:
- Automating code generation for data scraping scripts
- AI-assisted analysis of public datasets
- Generating reports or visualizations from intelligence data
- Debugging custom OSINT tools and scripts

Use Gemini CLI to enhance productivity in OSINT development by leveraging AI for code suggestions, refactoring, and problem-solving.