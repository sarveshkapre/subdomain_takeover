import subprocess
from typing import List


def run_amass(domain: str) -> List[str]:
    commands = [
        ["amass", "enum", "-passive", "-d", domain, "-o", "amass_passive.txt"],
        ["amass", "enum", "-brute", "-min-for-recursive", "2", "-d", domain, "-o", "amass_brute.txt"],
        ["amass", "enum", "-t", "reverseip", "-d", domain, "-o", "amass_reverseip.txt"]
    ]

    subdomains = []

    for command in commands:
        try:
            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(f"Error running Amass: {e.stderr.decode().strip()}")
            continue

        with open(command[-1], "r") as f:
            results = [line.strip() for line in f]

        subdomains.extend(results)

    return list(set(subdomains))


if __name__ == "__main__":
    domain = input("Enter the domain to brute-force: ").strip()
    subdomains = run_amass(domain=domain)
    print(f"Found {len(subdomains)} subdomains.")
