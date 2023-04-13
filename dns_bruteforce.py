import dns.resolver
import itertools

def load_wordlist(filename: str) -> list[str]:
    with open(filename, 'r') as file:
        wordlist = [line.strip() for line in file.readlines()]
    return wordlist

def dns_bruteforce(domain: str, wordlist: str) -> list[str]:
    resolver = dns.resolver.Resolver()
    subdomains = []

    for subdomain in wordlist:
        try:
            target = f"{subdomain}.{domain}"
            answers = resolver.resolve(target)
            if answers:
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
