import requests
import time
from typing import List


def ct_logs_crtsh(domain: str) -> List[str]:
    """
    This function ct_logs_crtsh() takes a domain as input and queries the crt.sh API to retrieve subdomains associated with SSL/TLS certificates.
    The subdomains are then added to a list and returned by the function.
    """
    subdomains = set()

    # Add wildcard to the domain name to get more results
    query = f"%25.{domain}"
    url = f"https://crt.sh/?q={query}&output=json"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for cert in data:
                # Filter the results to reduce false positives
                if cert["issuer_name"].startswith("CN=") and cert["not_after"] > int(time.time()):
                    names = cert["name_value"].split("\n")
                    subdomains.update(names)
    except Exception as e:
        print(f"Error querying crt.sh: {e}")

    return list(subdomains)


if __name__ == "__main__":
    domain = input("Enter the domain to brute-force: ").strip()
    subdomains = ct_logs_crtsh(domain=domain)
    print(f"Found {len(subdomains)} subdomains.")
