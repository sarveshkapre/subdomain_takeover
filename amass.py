# amass.py
import subprocess
from typing import List


def run_amass(domain: str) -> List[str]:
    command = ["amass", "enum", "-d", domain, "-o", "amass_output.txt"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    if process.returncode != 0:
        print(f"Error running Amass: {stderr.decode().strip()}")
        return []

    with open("amass_output.txt", "r") as f:
        subdomains = [line.strip() for line in f.readlines()]

    return subdomains
