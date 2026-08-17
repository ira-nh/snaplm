import platform
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


def get_python():
    return {
        "version": platform.python_version(),
    }

def get_hardware_info():
    return {
        "os": get_os(),
        "cpu": get_cpu(),
        "memory": get_memory(),
        "python": get_python(),
    }

{
    "system": {
        "os": "",
        "version": "",
        "architecture": "",
    },

    "cpu": {
        "name": "",
        "physical_cores": "",
        "logical_cores": "",
    },

    "memory": {
        "total_gb": 0,
        "available_gb": 0,
        "used_gb": 0,
        "percent_used": 0,
    },

    "python": {
        "version": "",
    }
    
}