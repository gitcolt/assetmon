import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os
import re

class CrtdotshSubdomainFinder:
    def grab_crtdotsh_subdomains_for_domain(domain):

        try:
            api_url = f'https://crt.sh/?q=%25.{domain}&output=json'
            api_response = requests.get(api_url, verify=False).json()
            subdomains = []
            for obj in api_response:
                subdomain_name = obj['name_value']
                match = re.search('\*', subdomain_name)
                if not match and subdomain_name not in subdomains:
                    subdomains.append(obj['name_value'])
            return subdomains
        except Exception as e:
            print(e)
