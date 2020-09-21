for domain in open('names.txt'):
    domain = domain.strip()
    cmd = "dnstwist --registered --ssdeep --geoip --all --threads 1 --whois --tld /Users/rogerioluz/Documents/XPi/rogerio/dnstwist/tld.txt --output /Users/rogerioluz/Documents/XPi/rogerio/dnstwist/files/{}.json --format json {}".format(domain, domain)
    print(cmd)