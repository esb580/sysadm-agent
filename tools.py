import subprocess


def check_disk_usage():
    """Run df -h and return the output."""
    result = subprocess.run(["df", "-h"], capture_output=True, text=True)
    return result.stdout
