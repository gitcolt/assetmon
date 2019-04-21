from flask import Blueprint, render_template, request, url_for, redirect
from assetmon.forms import AddDomainForm, RemoveDomainForm
from assetmon.models import db, Domain, Subdomain
from assetmon.managers.subdomain_discovery import grab_subdomains_for_domain, subdomain_already_found
import requests

bp = Blueprint('bp', __name__)

def send_notification(subdomain):
    requests.post('https://hooks.slack.com/services/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', json = {'text' : f'New subdomain found: {subdomain}'})


@bp.route('/')
def index():
    domains = Domain.query.all()
    add_domain_form = AddDomainForm()
    remove_domain_form = RemoveDomainForm()
    return render_template('index.html', 
            add_domain_form=add_domain_form, 
            remove_domain_form=remove_domain_form,
            all_domains=domains)

@bp.route('/api/add_domain', methods=['POST'])
def add_domain():
    domain_name = request.form['domain']
    domain = Domain(domain=domain_name, subdomain_search_ran=False)
    db.session.add(domain)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
    return redirect(url_for('bp.index'))

@bp.route('/api/remove_domain', methods=['POST'])
def remove_domain():
    domain_name = request.form['domain']
    domain = Domain.query.filter_by(domain=domain_name).first()
    db.session.delete(domain)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
    return redirect(url_for('bp.index'))

@bp.route('/api/find_new_subdomains', methods=['GET'])
def find_new_subdomains():
    monitored_domains = Domain.query.all()
    results = ''
    for domain in monitored_domains:
        first_run = not domain.subdomain_search_ran
        subdomain_names = grab_subdomains_for_domain(domain.domain)
        for subdomain_name in subdomain_names:
            if not subdomain_already_found(subdomain_name):
                if not first_run:
                    send_notification(subdomain_name)
                subdomain = Subdomain(subdomain=subdomain_name, domain_id=domain.id)
                db.session.add(subdomain)
                db.session.commit()
        if first_run:
            domain.subdomain_search_ran = True
            db.session.commit()
        results += str(subdomain_names)
    return results

