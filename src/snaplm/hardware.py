import platform
import psutil

def get_hardware_info():
    return {
        "system": platform.system(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "memory_gb": round(psutil.virtual_memory().total/(1024**3),2),
    }