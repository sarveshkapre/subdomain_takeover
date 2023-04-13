import requests

def ct_logs_crtsh(domain: str) -> list[str]:
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    subdomains = []

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
