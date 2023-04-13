import requests

def ct_logs_crtsh(domain: str) -> list[str]:
    """
    This function ct_logs_crtsh() takes a domain as input and queries the crt.sh API to retrieve subdomains associated with SSL/TLS certificates.
    The subdomains are then added to a list and returned by the function.
    """
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    subdomains = []

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for cert in data:
                for name in cert['name_value'].split('\n'):
                    if name not in subdomains:
                        subdomains.append(name)
    except Exception as e:
        print(f"Error querying crt.sh: {e}")

    return subdomains
