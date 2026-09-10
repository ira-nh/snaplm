import json
import platform
import subprocess

import psutil

def get_os():
    return {
        "name": platform.system(),
        "version": platform.release(),
        "architecture": platform.machine(),
    }


def get_cpu():
    return {
        "name": platform.processor(),
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),
    }


def get_memory():
    memory = psutil.virtual_memory()

    return {
        "total_gb": round(memory.total / (1024**3), 2),
        "available_gb": round(memory.available / (1024**3), 2),
        "used_gb": round(memory.used / (1024**3), 2),
        "percent_used": memory.percent,
    }

def get_gpu():
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        """
        Get-CimInstance Win32_VideoController |
        Select-Object Name, AdapterCompatibility, DriverVersion, Status |
        ConvertTo-Json
        """,
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True,
    )

    gpu = json.loads(result.stdout)

    return {
        "name": gpu["Name"],
        "vendor": gpu["AdapterCompatibility"],
        "driver_version": gpu["DriverVersion"],
        "status": gpu["Status"],
    }

def get_python():
    return {
        "version": platform.python_version(),
    }

def get_hardware_info():
    return {
        "os": get_os(),
        "cpu": get_cpu(),
        "memory": get_memory(),
        "gpu": get_gpu(),
        "python": get_python(),
    }

