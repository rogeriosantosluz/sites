from flask import Flask, render_template, request, redirect, flash, url_for, session, g
from . import app
from . import db
from .models import Domains, DNSTwist

@app.route("/")
def home():
    #metrics(request, session)
    app.logger.info("Home")
    return render_template("home.html")

@app.route("/sites")
def sites():
    #metrics(request, session)
    domains = Domains.query.all()
    query = db.session.query(DNSTwist.domain.distinct().label("domain"))
    dnstwist_domains = [row.domain for row in query.all()]
    #app.logger.info("dnstwist_domains: {}".format(dnstwist_domains))
    app.logger.info("Sites")
    return render_template("sites.html", domains=domains, dnstwist_domains=dnstwist_domains)

@app.route("/dnstwist")
def dnstwist():
    #metrics(request, session)
    domain = request.args.get("domain")
    app.logger.info("Domain: {}".format(domain))
    if domain:
        dnstwist = DNSTwist.query.filter_by(domain=domain).all()
    else:
        dnstwist = DNSTwist.query.all()
    app.logger.info("DNSTwist")
    return render_template("dnstwist.html", dnstwist=dnstwist)

@app.route("/fp/")
def fp():
    #app.logger.info("GGGGGGGGG")
    session["fingerprint"] = request.args.get("fp")
    return "OK"

def to_index():
    return redirect(url_for('home'))

@app.before_request
def login_handle():
    g.logged_in = bool(session.get('logged_in'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    app.logger.info('Login')
    if session.get('logged_in'):
        flash("You are already logged in")
        return to_index()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if (username == app.config['ADMIN_USERNAME'] and
            password == app.config['ADMIN_PASSWORD']):
            session['logged_in'] = True
            flash("Successfully logged in")
            return to_index()
        else:
            flash("Those credentials were incorrect")
    return render_template('login.html')


@app.route('/logout')
def logout():
    if session.get('logged_in'):
        session['logged_in'] = False
        flash("Successfully logged out")
    else:
        flash("You weren't logged in to begin with")
    return to_index()