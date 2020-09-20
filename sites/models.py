from . import db
import datetime

class Domains(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #RFC 1035 states that the maximum length of a DNS label is 63 characters. The Subdomain module schema has a textfield for the subdomain value with a maximum length of 255
    domain_name = db.Column(db.String(255), unique=True, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)