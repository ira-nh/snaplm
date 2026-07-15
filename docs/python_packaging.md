# Python Packaging and Installation

## Why Packaging?

Initially, SnapLM was run directly through Python files:

```powershell
py src/snaplm/cli.py
```

This works during development, but it requires the user to know the location of the source code.

A properly packaged Python project allows users to run the application as a command:

```powershell
snaplm
```

This changes SnapLM from a collection of scripts into an installable application.

---

# TOML Files

## What is TOML?

TOML stands for **Tom's Obvious, Minimal Language**.

It is a configuration file format designed to be:

- Human-readable
- Easy to edit
- Easy for programs to parse

Other common configuration formats include:

- JSON
- YAML
- INI

Example TOML:

```toml
name = "snaplm"
version = "0.1.0"
```

Equivalent JSON:

```json
{
    "name": "snaplm",
    "version": "0.1.0"
}
```

---

# pyproject.toml

`pyproject.toml` is the modern configuration file used by Python projects.

It defines:

- Project metadata
- Dependencies
- Build system
- Command-line entry points

Previously, Python projects commonly used:

```text
setup.py
```

Modern Python packaging uses:

```text
pyproject.toml
```

because it separates configuration from executable Python code.

---

# SnapLM pyproject.toml Structure

## Build System

```toml
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"
```

This tells Python which tool should build and install the package.

---

## Project Information

```toml
[project]
name = "snaplm"
version = "0.1.0"
```

The project name and version are defined here.

The folder name does not determine the package name.

The project identity comes from:

```toml
name = "snaplm"
```

---

## Dependencies

```toml
dependencies = [
    "psutil",
    "typer"
]
```

These are external Python libraries required by SnapLM.

When another user installs SnapLM, these dependencies are installed automatically.

Current dependencies:

- `psutil` → hardware/system information
- `typer` → command-line interface framework

---

# Project Scripts

```toml
[project.scripts]
snaplm = "snaplm.cli:app"
```

This creates a terminal command.

The format is:

```text
command = package.module:function
```

For SnapLM:

```text
snaplm
   |
   v
snaplm.cli
   |
   v
app()
```

When the user runs:

```powershell
snaplm
```

Python executes:

```python
app()
```

inside:

```text
src/snaplm/cli.py
```

---

# Installing a Local Project

## Normal package installation

Example:

```powershell
pip install psutil
```

This searches PyPI for a package named `psutil` (from the Internet).

---

## Installing the current project

SnapLM was installed using:

```powershell
py -m pip install -e .
```

Breaking this down:

### `py -m pip`

Runs pip using the selected Python interpreter.

### `install`

Installs a Python package.

### `.`

Means:

> The current directory.

Pip searches the current folder for:

```text
pyproject.toml
```

and reads the project information.

### `-e`

Means:

> Editable install.

Instead of copying the project, Python creates a link to the source code.

This means changes to:

```text
src/snaplm/
```

are immediately reflected when running:

```powershell
snaplm
```

without reinstalling.

---

# Installation Process

Running:

```powershell
py -m pip install -e .
```

caused this process:

```text
Current directory
        |
        v
pyproject.toml
        |
        v
Project name: snaplm
        |
        v
Create command: snaplm
        |
        v
Connect command to snaplm.cli:app
```

---

# Current SnapLM Flow

```text
User
 |
 | snaplm
 v
CLI launcher
 |
 v
snaplm.cli
 |
 v
Typer app()
 |
 v
detect()
 |
 v
hardware.py
 |
 v
psutil
 |
 v
Hardware report
```

# Editable Install vs Normal Install

Normal install:

```powershell
pip install .
```

Copies the package into Python's installed packages.

Editable install:

```powershell
pip install -e .
```

Creates a development link.

Editable installs are useful while building software because code changes are immediately available.

---

The current command:

```powershell
snaplm
```

runs:

```text
SnapLM Hardware Report

system: Windows
architecture: ARM64
processor: Qualcomm Oryon CPU
memory_gb: 15.61
```

---

# Future Improvements

Possible next steps:

- Add multiple CLI commands:
  - `snaplm detect`
  - `snaplm benchmark`
  - `snaplm models`

- Detect GPU/NPU capabilities

- Add model compatibility checks

- Recommend models based on hardware

- Add benchmarking tools