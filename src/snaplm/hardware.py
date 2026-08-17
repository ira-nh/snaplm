import platform
import psutil

def get_hardware_info():
    return {
        "system": platform.system(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "memory_gb": round(psutil.virtual_memory().total/(1024**3),2),
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