import typer

from snaplm.hardware import get_hardware_info

# Create command system (CLI application)
app = typer.Typer(no_args_is_help=True)

# When the user types "detect", call this function
@app.command()
def detect():
    """
    Detect system hardware.
    """
    info = get_hardware_info()

    print("SnapLM Hardware Report")
    print("\n======================\n")

    for key, value in info.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    app()