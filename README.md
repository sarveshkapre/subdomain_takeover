# Subdomain Takeover Scanner

## Overview
This Python script helps detect subdomain takeovers by scanning a target domain for potentially vulnerable subdomains. It uses asyncio and aiohttp for asynchronous scanning, which allows for faster and more efficient checking of multiple subdomains simultaneously.

## Table of Contents

- [How it works](#How it works)
- [Installation](#installation)
- [Usage](#usage)
- [Improvements](#improvements)
- [Contributing](#contributing)
- [License](#license)

## How it works

The script performs the following steps:

1. It retrieves a list of subdomains for the target domain using DNS TXT records (if available).
2. It sends HTTP requests to each subdomain to fetch the content of the corresponding web page.
3. It checks the content of each fetched web page for known takeover identifiers (e.g., specific error messages or unique strings associated with third-party services).
4. If an identifier is found, the script flags the subdomain as potentially vulnerable to a takeover and adds it to the results.
5. The results are saved to a text file named <domain>_subdomain_takeovers.txt.

## Limitations and known issues

- The script relies on DNS TXT records for subdomain enumeration. If the target domain does not have a TXT record for subdomain enumeration, the script may not discover all subdomains.
- The current list of takeover identifiers is limited. You may need to update the identifiers.py file with additional identifiers for other third-party services.
- The script uses a fixed concurrency level (number of simultaneous tasks). Depending on your system's resources and the target domain's server capacity, you may need to adjust the concurrency level to avoid causing excessive load on the target server or your own system.

## Usage

To use the Subdomain Takeover Scanner, follow these steps:

1. Install the required dependencies mentioned in the requirements.txt file using the following command:

```bash
pip install -r requirements.txt
```

Run the script with:
```
python subdomain_takeover.py
```

When prompted, enter the domain you want to check for subdomain takeovers and press Enter. The script will generate a text file containing the results.

## Examples

To check for subdomain takeovers on example.com:

```
python subdomain_takeover.py
```

Enter the domain when prompted:

```
Enter the domain to check for subdomain takeovers: example.com
```

The script will run and save the results to a file named example.com_subdomain_takeovers.txt.

Note: Always ensure you have permission to scan the target domain, and adhere to ethical practices when using this script.


## Contributing

We welcome contributions to the Subdomain Takeover Scanner project! Feel free to submit pull requests or open issues with bug reports or feature requests. Before contributing, please read the Code of Conduct.

## License

This project is licensed under the MIT License.