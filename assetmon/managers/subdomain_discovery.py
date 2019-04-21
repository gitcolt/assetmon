from assetmon.models import db, Domain, Subdomain
from assetmon.managers.tools.threatcrowd import ThreatcrowdSubdomainFinder
from assetmon.managers.tools.virustotal import VirustotalSubdomainFinder
from assetmon.managers.tools.crtdotsh import CrtdotshSubdomainFinder

class SubdomainFinderAdapter(object):

    def __init__(self, tool, subdomain_grab_func):
        self.tool = tool
        self.grab_subdomains_for_domain = subdomain_grab_func

    def __getattr__(self, attr):
        return getattr(self.tool, attr)

def grab_subdomains_for_domain(domain):

    subdomains = []
    for adapter in subdomain_finder_adapters:
        asdf = adapter.grab_subdomains_for_domain(domain)
        if asdf == None:
            continue
        subdomains += asdf
    # Remove duplicates before querying database
    subdomains = list(dict.fromkeys(subdomains))
    return subdomains

def subdomain_already_found(subdomain):

    subdomain_in_db = Subdomain.query.filter_by(subdomain=subdomain).first()
    return False if subdomain_in_db == None else True

subdomain_finder_adapters = [
        SubdomainFinderAdapter(ThreatcrowdSubdomainFinder,
                ThreatcrowdSubdomainFinder.grab_threatcrowd_subdomains_for_domain),
        SubdomainFinderAdapter(VirustotalSubdomainFinder,
                VirustotalSubdomainFinder.grab_virustotal_subdomains_for_domain),
        SubdomainFinderAdapter(CrtdotshSubdomainFinder,
                CrtdotshSubdomainFinder.grab_crtdotsh_subdomains_for_domain)
]
