import asyncio
import aiohttp
from typing import List, Dict, Optional
from identifiers import IDENTIFIERS
from amass import run_amass
from dns_bruteforce import dns_bruteforce, load_wordlist
from dns_zone_transfer import dns_zone_transfer
from ct_logs import ct_logs_crtsh
import requests
from ssl import SSLSocket, create_default_context
from typing import Tuple
import dns.resolver
import ssl
import time
from typing import Dict, Tuple

PROJECT_URL = "https://github.com/example/subdomain_takeover"
USER_AGENT = f"SubdomainTakeoverScanner/1.0 (+{PROJECT_URL})"


async def check_subdomain_takeover(url: str, sem: asyncio.Semaphore) -> Optional[str]:
    async with sem:
        headers = {"User-Agent": USER_AGENT}
        async with aiohttp.ClientSession(headers=headers) as session:
            try:
                async with session.get(url, timeout=5) as response:
                    content = await response.text()
            except Exception as e:
                print(f"Error fetching {url}: {e}")
                return None

    for host, (search_domain, identifier) in IDENTIFIERS.items():
        if search_domain in url and identifier in content:
            return host

    return None


def verify_ownership(subdomain: str, provider: str) -> bool:
    # Replace this placeholder with the actual provider API interaction logic.
    api_key = "your_api_key"
    headers = {"Authorization": f"Bearer {api_key}"}

    # Depending on the provider's specific API and authentication method, you may need to adjust this request.
    response = requests.get(
        f"https://example.com/api/v1/check_ownership?subdomain={subdomain}",
        headers=headers,
    )

    if response.status_code == 200:
        return response.json()["ownership"]
    else:
        return False


async def check_orphaned_expired_subdomains(
    subdomain: str, sem: asyncio.Semaphore
) -> bool:
    async with sem:
        # Replace this placeholder with the actual logic to check if the subdomain is orphaned or expired.
        response = await aiohttp.get(f"https://{subdomain}")

        if response.status == 404:
            return True
        else:
            return False


async def validate_certificates(
    subdomain: str, sem: asyncio.Semaphore
) -> Tuple[str, bool]:
    async with sem:
        context = create_default_context()
        try:
            with SSLSocket(context=context) as sock:
                sock.connect((subdomain, 443))
                cert = sock.getpeercert()
            # Check the certificate's expiration date, issuer, and other relevant information.
            # Return subdomain and True if the certificate is valid and properly configured, False otherwise.
            return (subdomain, True)
        except Exception as e:
            print(f"Error checking certificate for {subdomain}: {e}")
            return (subdomain, False)


def get_dns_records(subdomain: str) -> Dict[str, str]:
    records = {}
    try:
        answers = dns.resolver.resolve(subdomain, "A")
        records["A"] = str(answers[0])
    except:
        records["A"] = None

    try:
        answers = dns.resolver.resolve(subdomain, "AAAA")
        records["AAAA"] = str(answers[0])
    except:
        records["AAAA"] = None

    return records


def get_tls_certificate(subdomain: str) -> Tuple[str, str]:
    context = ssl.create_default_context()
    try:
        with ssl.SSLSocket(context=context) as sock:
            sock.connect((subdomain, 443))
            cert = sock.getpeercert()
        issuer = cert["issuer"]
        not_after = cert["notAfter"]
        return (issuer, not_after)
    except Exception as e:
        return (None, None)


def monitor_dns_tls_changes(subdomain: str, check_interval: int = 3600) -> bool:
    baseline_dns = get_dns_records(subdomain)
    baseline_cert = get_tls_certificate(subdomain)

    while True:
        time.sleep(check_interval)

        current_dns = get_dns_records(subdomain)
        current_cert = get_tls_certificate(subdomain)

        if current_dns != baseline_dns:
            print(f"DNS records changed for {subdomain}")
            return True

        if current_cert != baseline_cert:
            print(f"TLS certificate changed for {subdomain}")
            return True

    return False


async def find_subdomain_takeovers(domain: str) -> Dict[str, List[str]]:
    # Amass subdomains
    amass_subdomains = run_amass(domain)

    # DNS brute-forcing
    wordlist_filename = "wordlist.txt"
    wordlist = load_wordlist(wordlist_filename)
    brute_force_subdomains = dns_bruteforce(domain, wordlist)

    # DNS zone transfers
    zone_transfer_subdomains = dns_zone_transfer(domain)

    # Certificate Transparency logs
    ct_subdomains = ct_logs_crtsh(domain)

    # Combine all subdomains
    subdomains = list(
        set(
            amass_subdomains
            + brute_force_subdomains
            + zone_transfer_subdomains
            + ct_subdomains
        )
    )

    takeovers = {}
    sem = asyncio.Semaphore(
        10
    )  # Set the concurrency level (number of simultaneous tasks)

    tasks = []
    for subdomain in subdomains:
        for protocol in ("http", "https"):
            url = f"{protocol}://{subdomain}"
            tasks.append(asyncio.ensure_future(check_subdomain_takeover(url, sem)))

        # Add the new functions to the tasks list.
        tasks.append(
            asyncio.ensure_future(check_orphaned_expired_subdomains(subdomain, sem))
        )
        tasks.append(asyncio.ensure_future(validate_certificates(subdomain, sem)))

        # Add a separate task for monitoring subdomains.
        # This should be run periodically, possibly in a separate process or using a scheduler.
        # monitor_dns_tls_changes(subdomain)

    results = await asyncio.gather(*tasks)

    for i, provider in enumerate(results):
        if provider:
            if provider not in takeovers:
                takeovers[provider] = []
            takeovers[provider].append(tasks[i]._coro.cr_frame.f_locals["url"])

    return takeovers


async def main():
    domain = input("Enter the domain to check for subdomain takeovers: ").strip()
    takeovers = await find_subdomain_takeovers(domain)
    filename = f"{domain}_subdomain_takeovers.txt"

    with open(filename, "w") as f:
        for provider, urls in takeovers.items():
            f.write(f"Possible {provider} takeovers:\n")
            for url in urls:
                f.write(f"{url}\n")
            f.write("\n")

    print(f"Subdomain takeover results written to {filename}")


if __name__ == "__main__":
    asyncio.run(main())
