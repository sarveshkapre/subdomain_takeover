# Subdomain Takeover Scanner

The Subdomain Takeover Scanner is a Python-based tool that uses multiple techniques to enumerate and identify subdomains vulnerable to subdomain takeovers. It combines the results of these techniques to provide a comprehensive list of subdomains, which are then checked for potential takeover vulnerabilities. This document explains how the code runs and the techniques used in the project.

## Table of Contents

- [Overview](#overview)
- [Subdomain Enumeration Techniques](#subdomain-enumeration-techniques)
  - [Amass](#amass)
  - [DNS Brute-forcing](#dns-brute-forcing)
  - [DNS Zone Transfers](#dns-zone-transfers)
  - [Certificate Transparency Logs](#certificate-transparency-logs)
- [Checking Subdomains for Takeovers](#checking-subdomains-for-takeovers)
- [Generating a Report](#generating-a-report)
- [Usage](#usage)
- [Limitations and Known Issues](#limitations-and-known-issues)
- [Extending Functionality](#extending-functionality)
- [Contributing](#contributing)
- [License](#license)


## Overview

The main steps in the Subdomain Takeover Scanner are:

1. Enumerate subdomains using multiple techniques.
2. Check the enumerated subdomains for potential subdomain takeovers.
3. Generate a report with the results.

## Subdomain Enumeration Techniques

The scanner uses the following techniques to enumerate subdomains:

### Amass

Amass is an open-source subdomain enumeration tool that performs DNS enumeration, scraping, and other techniques to discover subdomains. The `run_amass()` function in `amass.py` runs the Amass binary and returns the discovered subdomains.

### DNS Brute-forcing

DNS brute-forcing is the process of guessing subdomains by trying common prefixes or words. The `dns_bruteforce()` function in `dns_bruteforce.py` takes a domain and a wordlist as input and performs DNS resolution on each word, combined with the domain, to discover valid subdomains. The `load_wordlist()` function reads a wordlist file and returns a list of words.

### DNS Zone Transfers

DNS zone transfers (AXFR queries) are used to replicate DNS databases across DNS servers. If a domain's DNS server allows zone transfers, it can reveal all the domain's subdomains. The `dns_zone_transfer()` function in `dns_zone_transfer.py` attempts a zone transfer and returns the discovered subdomains.

### Certificate Transparency Logs

Certificate Transparency (CT) logs are public, append-only records of issued SSL/TLS certificates. Querying CT logs can reveal subdomains associated with certificates. The `ct_logs_crtsh()` function in `ct_logs.py` queries the crt.sh API to find subdomains related to the given domain.

## Checking Subdomains for Takeovers

After enumerating subdomains, the scanner checks each subdomain for potential subdomain takeovers using the `check_subdomain_takeover()` function. It sends HTTP and HTTPS requests to each subdomain and looks for specific patterns (identifiers) in the content that indicate the subdomain may be vulnerable to a takeover. The identifiers are defined in the `identifiers.py` file.

## Generating a Report

The scanner generates a report with the results, listing potential takeovers by provider, and saves it to a text file. The `main()` function handles user input, calls the `find_subdomain_takeovers()` function, and writes the report.

## Limitations and known issues

- The script relies on DNS TXT records for subdomain enumeration. If the target domain does not have a TXT record for subdomain enumeration, the script may not discover all subdomains.
- The current list of takeover identifiers is limited. You may need to update the identifiers.py file with additional identifiers for other third-party services.
- The script uses a fixed concurrency level (number of simultaneous tasks). Depending on your system's resources and the target domain's server capacity, you may need to adjust the concurrency level to avoid causing excessive load on the target server or your own system.

## Usage

To run the scanner, execute the `subdomain_takeover.py` script and provide the target domain when prompted. The scanner will perform subdomain enumeration, check for potential takeovers, and generate a report with the results.

1. Install the required dependencies mentioned in the requirements.txt file using the following command:

```bash
pip install -r requirements.txt
```

Run the script with:
```
python subdomain_takeover.py
```

The results will be written to a file named <domain>_subdomain_takeovers.txt.

## Extending Functionality

- You can extend the script's functionality by implementing additional subdomain enumeration methods or modifying existing ones. 
- The script is designed to be modular, allowing you to easily add new methods as needed.

## Limitations and Known Issues

- The script may produce false positives or negatives due to the nature of subdomain takeover detection.
- The performance of the script may be affected by the size of the wordlist used for DNS brute-forcing.
- DNS zone transfers may not be allowed by the target domain's DNS server.


## Contributing

We welcome contributions to the Subdomain Takeover Scanner project! Feel free to submit pull requests or open issues with bug reports or feature requests. Before contributing, please read the Code of Conduct.

## License

This project is licensed under the MIT License.