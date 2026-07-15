# CLI Design

## Goal

Create a command line interface for SnapLM so users can interact with the tool through simple terminal commands

Example:

```powershell
snaplm detect
```
## Why a CLI

While SnapLM was initially tested via Python scripts:

```powershell
py experiments/test_hardware.py
```
This works for development but isn't ideal for users, so a CLI would be more useful to allow users to interact with SnapLM without needing to burden themselves with the internal file structure.

## CLI Architecture so far

### cli.py
- Receives user commands
- Formats the output
- Calls the appropriate functions

### hardware.py
- Detects system information
- Runs structured data
- Does not handle user interaction

## Typer vs argparse

`argparse` is Python's inbuilt command line parsing library. However, it is more boilerplate and thus is more difficult to maintain as commands increase.
Future commands to create, such as:
```
snaplm detect
snaplm benchmark
snaplm download
snaplm models
```
would require significantly more set up.

In comparison, Typer is a modern Python CLI framework that uses the modern Click library.
It uses Python type hints, cleaner command definitions, easier scaling to multiple commands and has help generation. For example:
```Python
@app.command()
def detect():
    ...
```
creates a CLI command from a Python function.

## Decision

Typer was chosen because SnapLM is intended to grow into a multi-command tool. A CLI framework that scales well will make future development easier.

## Current Output

Command:
```Powershell
py src/snaplm/cli.py
```

Output:
```
SnapLM Hardware Report

======================

system: Windows
architecture: ARM64
processor: ARMv8 (64-bit) Family 8 Model 1 Revision 201, Qualcomm Technologies Inc
memory_gb: 15.61
```

## Future improvements:
- Better formatted reports
- JSON output option
- Multiple CLI commands
- Package SnapLM as an installable command