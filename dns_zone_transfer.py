import dns.query
import dns.zone

def dns_zone_transfer(domain: str) -> list[str]:
    resolver = dns.resolver.Resolver()
    subdomains = []

    try:
        ns_answers = resolver.resolve(domain, 'NS')
        for ns_rrset in ns_answers:
            ns_name = ns_rrset.target.to_text()[:-1]
            zone = dns.zone.from_xfr(dns.query.xfr(ns_name, domain, timeout=5))
            for name, node in zone.nodes.items():
                if name != '@':
                    subdomain = f"{name}.{domain}"
                    subdomains.append(subdomain)
                    print(f"Found subdomain: {subdomain}")

    except dns.resolver.NoNameservers:
        print("No nameservers found for the domain.")
    except dns.exception.Timeout:
        print("DNS zone transfer timed out.")
    except Exception as e:
        print(f"Error during DNS zone transfer: {e}")

    return subdomains

if __name__ == "__main__":
    domain = input("Enter the domain to check for zone transfers: ").strip()
    subdomains = dns_zone_transfer(domain)
    print(f"Found {len(subdomains)} subdomains.")
