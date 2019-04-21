import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os

class VirustotalSubdomainFinder:
    def grab_virustotal_subdomains_for_domain(domain):

        try:
            key = os.environ['VIRUSTOTAL_API_KEY']
            api_url = f'https://www.virustotal.com/vtapi/v2/domain/report?apikey={key}&domain={domain}'
            api_response = requests.get(api_url, verify=False)
            subdomains = api_response.json()['subdomains']
            return subdomains
        except Exception as e:
            print(e)
