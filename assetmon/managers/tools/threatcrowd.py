import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import re

class ThreatcrowdSubdomainFinder:
    def grab_threatcrowd_subdomains_for_domain(domain):

        try:
            api_url = f'http://www.threatcrowd.org/searchApi/v2/domain/report/?domain={domain}'
            api_response = requests.get(api_url, verify=False)
            subdomains = api_response.json()['subdomains']
            for (index, subdomain) in enumerate(subdomains):
                match = re.search('^\.', subdomain)
                if match:
                    del subdomains[index]
            return subdomains
        except Exception as e:
            print(e)
