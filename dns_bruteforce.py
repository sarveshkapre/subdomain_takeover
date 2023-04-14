import dns.resolver
from typing import List

def load_wordlist(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        wordlist = [line.strip() for line in file.readlines()]
    return wordlist

def dns_bruteforce(domain: str, wordlist: List[str]) -> List[str]:
    resolver = dns.resolver.Resolver()
    subdomains = []

    for subdomain in wordlist:
        target = f"{subdomain}.{domain}"
        try:
            resolver.resolve(target)  # Check if the target subdomain resolves to any IP address
            subdomains.append(target)
            print(f"Found subdomain: {target}")
        except dns.resolver.NXDOMAIN:
            pass
        except Exception as e:
            print(f"Error resolving {target}: {e}")

    return subdomains

if __name__ == "__main__":
    domain = input("Enter the domain to brute-force: ").strip()
    wordlist_filename = input("Enter the wordlist filename: ").strip()
    wordlist = load_wordlist(wordlist_filename)
    subdomains = dns_bruteforce(domain, wordlist)
    print(f"Found {len(subdomains)} subdomains.")
