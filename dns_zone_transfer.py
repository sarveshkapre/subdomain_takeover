import dns.query
import dns.zone
import dns.resolver
from typing import List
from multiprocessing import Pool


def dns_zone_transfer(domain: str) -> List[str]:
    # Create a dns.resolver.Resolver object to resolve the nameservers for the given domain.
    resolver = dns.resolver.Resolver()
    subdomains = []

    try:
        ns_answers = resolver.resolve(domain, 'NS')
    except dns.resolver.NoNameservers:
        print("No nameservers found for the domain.")
        return subdomains
    except Exception as e:
        print(f"Error resolving nameservers: {e}")
        return subdomains

    # Iterate through the nameserver records (ns_answers) and strip the trailing dot from the nameserver name using ns_name = ns_rrset.target.to_text().rstrip('.').
    for ns_rrset in ns_answers:
        ns_name = ns_rrset.target.to_text().rstrip('.')
        try:
            # For each nameserver, attempt to perform a DNS zone transfer using dns.zone.from_xfr(dns.query.xfr(ns_name, domain, timeout=30)).
            # Use a larger timeout value (30 seconds) to account for slow network connections and large domains.
            zone = dns.zone.from_xfr(dns.query.xfr(ns_name, domain, timeout=30))
        except dns.query.TransferError:
            print(f"Transfer error for nameserver {ns_name}.")
            continue
        except dns.exception.Timeout:
            print(f"DNS zone transfer timed out for nameserver {ns_name}.")
            continue
        except Exception as e:
            print(f"Error during DNS zone transfer for nameserver {ns_name}: {e}")
            continue

        for name, node in zone.nodes.items():
            if name != '@':
                subdomain = f"{name}.{domain}"
                # Verify that each subdomain is actually valid before adding it to the list of results.
                try:
                    answers = resolver.query(subdomain)
                    if answers:
                        subdomains.append(subdomain)
                        print(f"Found subdomain: {subdomain}")
                except:
                    continue

    return subdomains


if __name__ == "__main__":
    domain = input("Enter the domain to check for zone transfers: ").strip()
    
    # Use multiprocessing to speed up the enumeration.
    with Pool() as pool:
        subdomains = pool.map(dns_zone_transfer, [domain])

    # Flatten the list of subdomains.
    subdomains = [subdomain for sublist in subdomains for subdomain in sublist]

    print(f"Found {len(subdomains)} subdomains.")
