import subprocess

def detect_ollama():
    try:
        result = subprocess.run(
            ["ollama","--version"],
            capture_output=True,
            text=True,
            check=True,
        )

        return {
            "installed": True,
            "version": result.stdout.strip().split()[-1]
        }

    except FileNotFoundError:
        return {
            "installed": False,
            "version": None,
        }

# subprocess.run(...) means run another program in Python
# capture_output=True means give terminal output back to Python
# using try/except in EAFP python style