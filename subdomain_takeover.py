import asyncio
import aiohttp
from dns import resolver
from dns.exception import DNSException
from typing import List, Dict, Optional
from identifiers import IDENTIFIERS

USER_AGENT = "SubdomainTakeoverScanner/1.0 (+https://github.com/yourusername/subdomain-takeover-scanner)"


def get_subdomains(domain: str) -> List[str]:
    subdomains = set()
    try:
        answers = resolver.resolve(f'_subdomain_enum.{domain}', 'TXT')
        for rdata in answers:
            subdomains |= set(rdata.strings[0].decode().split(','))
    except DNSException as e:
        print(f"Error resolving subdomains: {e}")

    return list(subdomains)


async def check_subdomain_takeover(url: str, sem: asyncio.Semaphore) -> Optional[str]:
    async with sem:
        headers = {'User-Agent': USER_AGENT}
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


async def find_subdomain_takeovers(domain: str) -> Dict[str, List[str]]:
    subdomains = get_subdomains(domain)
    takeovers = {}
    sem = asyncio.Semaphore(10)  # Set the concurrency level (number of simultaneous tasks)

    tasks = []
    for subdomain in subdomains:
        for protocol in ('http', 'https'):
            url = f"{protocol}://{subdomain}.{domain}"
            tasks.append(asyncio.ensure_future(check_subdomain_takeover(url, sem)))

    results = await asyncio.gather(*tasks)

    for i, provider in enumerate(results):
        if provider:
            if provider not in takeovers:
                takeovers[provider] = []
            takeovers[provider].append(tasks[i]._coro.cr_frame.f_locals['url'])

    return takeovers


async def main():
    domain = input("Enter the domain to check for subdomain takeovers: ").strip()
    takeovers = await find_subdomain_takeovers(domain)
    filename = f"{domain}_subdomain_takeovers.txt"

    with open(filename, 'w') as f:
        for provider, urls in takeovers.items():
            f.write(f"Possible {provider} takeovers:\n")
            for url in urls:
                f.write(f"{url}\n")
            f.write("\n")

    print(f"Subdomain takeover results written to {filename}")


if __name__ == "__main__":
    asyncio.run(main())
