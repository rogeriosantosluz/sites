from . import db
import datetime

class Domains(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #RFC 1035 states that the maximum length of a DNS label is 63 characters. The Subdomain module schema has a textfield for the subdomain value with a maximum length of 255
    domain_name = db.Column(db.String(255), unique=True, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)


"""
flask shell

>>> from sites import db
>>> from sites.models import Domains
>>> db.session.add(Domains(domain_name="xpi.com.br"))
>>> db.session.commit()

"""

class DNSTwist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(255), nullable=False)
    #RFC 1035 states that the maximum length of a DNS label is 63 characters. The Subdomain module schema has a textfield for the subdomain value with a maximum length of 255
    domain_name = db.Column(db.String(255), unique=True, nullable=False)
    dns_a = db.Column(db.String(255), nullable=True)
    dns_aaaa = db.Column(db.String(255), nullable=True)
    fuzzer = db.Column(db.String(255), nullable=True)
    geoip_country = db.Column(db.String(255), nullable=True)
    ssdeep_score = db.Column(db.String(255), nullable=True)
    dns_ns = db.Column(db.String(255), nullable=True)
    dns_mx = db.Column(db.String(255), nullable=True)
    whois_created = db.Column(db.String(255), nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)