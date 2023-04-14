# Subdomain Takeovers: A guide to Detection and Prevention

## Table of Contents
- [Introduction](#introduction)
- [Details](#details)
- [Techniques for Detecting and Preventing Subdomain Takeovers](#techniques-for-detecting-and-preventing-subdomain-takeovers)
  - [Method 1: DNS Enumeration with Amass](#method-1-dns-enumeration-with-amass)
  - [Method 2: DNS Brute Force with Knock](#method-2-dns-brute-force-with-knock)
  - [Method 3: DNS Zone Transfer with Dnsrecon](#method-3-dns-zone-transfer-with-dnsrecon)
  - [Method 4: Monitoring Certificate Transparency Logs](#method-4-monitoring-certificate-transparency-logs)
- [Best Practices for Preventing Subdomain Takeovers](#best-practices-for-preventing-subdomain-takeovers)
- [Limitations and Challenges](#limitations-and-challenges)
- [Conclusion](#conclusion)


## Introduction

Subdomain takeover is a growing threat to organizations of all sizes, and it can result in serious consequences such as data theft, website defacement, and loss of revenue. Attackers can take advantage of subdomains that are no longer in use but still have DNS records pointing to cloud services like AWS and Heroku that are not properly configured. By taking over these subdomains, attackers can host their own content or carry out phishing attacks, posing a serious risk to organizations.

In this blog post, we'll explore various techniques for detecting and preventing subdomain takeovers, as well as best practices for protecting your organization from this significant threat.

## Details

Subdomain takeovers can be thought of as a result of misconfigurations or oversight in an organization's DNS records and infrastructure. When a subdomain is created for a particular service or purpose, it is added to the organization's DNS records and mapped to a specific IP address. However, if that service or purpose is no longer needed or has been moved to a different platform, the subdomain may be forgotten and left in the DNS records, but with no associated IP address. This creates an opportunity for attackers to take control of the subdomain by creating a matching service or platform, and then manipulating the DNS records to map the subdomain to their own IP address.

To approach subdomain takeovers from a cybersecurity perspective, there are several key learnings that can be applied. First, it's important to regularly monitor DNS records and ensure that any subdomains that are no longer needed are removed. This can prevent attackers from exploiting forgotten subdomains to gain access to an organization's assets. Additionally, it's important to regularly test for vulnerabilities in web applications and infrastructure that could be exploited to take over subdomains.

Another important learning is to stay informed about the latest techniques and tools that attackers are using to discover and exploit subdomain takeover vulnerabilities. By monitoring security forums and following the latest research in this area, organizations can stay one step ahead of potential attackers and implement effective prevention and detection strategies.

From a technical perspective, it's important to have a comprehensive approach to detecting and preventing subdomain takeovers. This may involve using a combination of techniques such as DNS enumeration, passive DNS monitoring, scanning for open ports and services, analyzing certificate transparency logs, and using web application vulnerability scanners. Additionally, organizations should prioritize educating employees on the risks of subdomain takeover and phishing attacks, and encourage them to report any suspicious activity.

In summary, to approach subdomain takeovers from a first principles perspective, it's important to understand the underlying causes of these vulnerabilities and develop a comprehensive approach to detection and prevention. By staying informed and implementing best practices for DNS management, web application security, organizations can reduce their risk of falling victim to subdomain takeovers and keep their assets secure.


## Techniques for Detecting and Preventing Subdomain Takeovers

### Method 1: DNS Enumeration with Amass

One effective technique for detecting subdomain takeovers is using a tool like Amass, which can be used to perform automated reconnaissance and identify subdomains that may be vulnerable to takeover. Amass uses a variety of methods, including active reconnaissance and passive intelligence gathering, to generate a comprehensive list of potential subdomains. Amass can also perform DNS queries to validate the existence of subdomains, making it an effective way to identify vulnerable targets for subdomain takeover.

Here's an example command that uses Amass to enumerate subdomains:

```
amass enum -d example.com -o output.txt
```

This command will output a list of subdomains for the specified domain, and save it to a file named output.txt.

### Method 2: DNS Brute Force with Knock

DNS brute force can also be used to generate a list of potential subdomains to target. Knock is a tool that can be used to perform DNS brute force and generate a list of potential subdomains. Knock uses a large wordlist of subdomain names and generates DNS queries to check if these subdomains exist.

Here's an example command that uses Knock to perform DNS brute force:

```
knockpy domain.com
```
This command will output a list of potential subdomains for the specified domain.

### Method 3: DNS Zone Transfer with Dnsrecon

DNS zone transfers can provide valuable information about a domain's configuration and potentially reveal subdomains that are not publicly accessible. Dnsrecon is a tool that can be used to perform DNS zone transfer and gather information about a domain's DNS configuration.

Here's an example command that uses Dnsrecon to perform DNS zone transfer:

```
dnsrecon -t axfr -d domain.com
```
This command will attempt to perform a DNS zone transfer for the specified domain.

### Method 4: Monitoring Certificate Transparency Logs

Monitoring certificate transparency logs can help detect unauthorized SSL/TLS certificates issued for a domain, which can indicate a subdomain takeover. Certificate transparency logs are public records of all SSL/TLS certificates issued by certificate authorities, and they can be searched to identify certificates that have been issued for a particular domain. By monitoring these logs, it's possible to detect unauthorized certificates that may be a sign of subdomain takeover.

Several online tools are available for monitoring certificate transparency logs, including:

- crt.sh
- Google Certificate Transparency Search

Best Practices for Preventing Subdomain Takeovers

In addition to using the above techniques for detecting subdomain takeovers, there are several best practices that organizations can follow to prevent subdomain takeovers:

- Remove DNS records for subdomains that are no longer in use
- Regularly scan and test for vulnerabilities in your organization's web applications and infrastructure
- Monitor DNS configuration for changes and inconsistencies
- Use strong passwords and two-factor authentication for DNS and cloud service accounts

## Limitations and Challenges

While the above techniques can be effective for detecting subdomain takeovers, there are some limitations and challenges to consider:

- DNS brute force can generate a large number of false positives, making it difficult to identify true vulnerabilities.
- These techniques may not be able to identify subdomains that are hosted on different IP addresses than the main domain or that are hidden behind a CDN or other proxy.
- Subdomain takeovers can be difficult to detect in real-time, which means that organizations may not be aware of the issue until after it has already happened.

## Conclusion

Subdomain takeover is a significant threat to organizations, and it's important to have effective detection and prevention strategies in place. By using a combination of techniques like DNS enumeration, DNS brute force, DNS zone transfer, and monitoring certificate transparency logs, organizations can improve their ability to detect subdomain takeovers and prevent them from happening in the first place. Additionally, following best practices for preventing subdomain takeovers and regularly testing for vulnerabilities can help ensure that your organization is protected from this growing threat.