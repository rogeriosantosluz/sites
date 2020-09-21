from . import db
from . import app
from .models import Domains, DNSTwist
import click

from flask import Blueprint

bp = Blueprint('utils', __name__)

@bp.cli.command('import_domains')
#@click.option('--file_path', type=click.STRING, help='Caminho completo do arquivo de dominios, que deve ter um dominio por linha')
@click.argument('filename', type=click.Path(exists=True))
def import_domains(filename):
    """ Importa os dominios para o sistema de sites \n
        ***IMPORTANTE*** \n
        FILENAME deve ser o caminho completo do arquivo de dominios, que deve ter um dominio por linha
    """
    for domain in open(filename):
        domain = domain.strip()
        app.logger.info("Importando... {}".format(domain))
        try:
            db.session.add(Domains(domain_name=domain))
            db.session.commit()
        except Exception as inst:
            app.logger.error(inst)
            db.session.rollback()
    

"""
flask shell

from sites import utils
utils.import_domains()

"""


"""
Metodo que le todos os arquivos json gerados em ROOT_DIR pelo seguinte comando dnstwist:

dnstwist 
    --registered 
    --ssdeep (algoritmo que determina o score de semelhanca entre a pagina original e a clone)
    --geoip (localizacao)
    --all 
    --threads 1 
    --whois 
    --tld ROOT_DIR/tld.txt (A top-level domain (TLD) is one of the domains at the highest level in the hierarchical Domain Name System of the Internet)
    --output ROOT_DIR/www.testadordabolsa.com.br.json 
    --format json 
    www.testadordabolsa.com.br

"""

@bp.cli.command('import_dnstwist')
@click.option('--directory_path', type=click.STRING, help='Caminho completo do diretorio com os arquivos JSON do dnstwist a serem importados')
def import_dnstwist(directory_path):
    """ Importa os arquivos JSON gerados pelo DNSTwist """
    app.logger.info("Iniciand0...") 
    import os
    import json

    ROOT_DIR = directory_path
    files = os.listdir(ROOT_DIR)
    app.logger.info(files)
    json_list = []
    for file in files:
        full_file = ROOT_DIR + file
        json_file = {"file": full_file, "domain": file.replace(".json", ""), "content" : {"domain": {} }}
        #print("##### FILE {} ######".format(full_file))
        str_json = ""
        for linha in open(full_file):
            #print(linha)
            if linha.strip() != "[39m[0m":
                str_json += linha
        if str_json:
            json_file["content"] = json.loads(str_json)
            json_list.append(json_file)
    #print(json_list)

    keys = []
    dominios = []
    for i in json_list:
        for c in i["content"]:
            for k in c.keys():
                if k not in keys:
                    #chaves utilizadas para definir a tabela
                    keys.append(k)
            #DNSTwinst retorna keys com "-", trocando para "_" para podemos usar dict no insert
            for a in keys:
                if a in c:
                    c[a.replace("-","_")] = c[a]
                    del c[a]
            #
            #De array para string por virgulas
            for ke, v in c.items():
                if isinstance(v, list):
                    c[ke] = ",".join(v)
            #
            if i["domain"] not in dominios:
                dominios.append(i["domain"])
            #app.logger.info("{} {} {} {}".format(i["domain"], c["domain_name"], c.get('geoip_country',''), c.get('ssdeep_score','')))#, c.get('whois-created',''), c.keys())
            c["domain"] = i["domain"]
            app.logger.info("{}".format(c))
            #Insert na tabela dnstwist
            try:
                db.session.add(DNSTwist(**c))
                db.session.commit()
            except Exception as inst:
                app.logger.error(inst)
                db.session.rollback()

    app.logger.info("Dominios encontrados: {}".format(dominios))
    app.logger.info("Quantidade de entradas: {} ".format(len(json_list)))
    #app.logger.info("Keys:{}".format(keys))


"""
flask shell

from sites import utils
utils.import_dnstwist()

INFO:sites:owa.tecfinance.com.br {'dns_a': ['46.30.215.237'], 'dns_aaaa': ['2a02:2350:5:107:806b:2ea6:9e63:17e8'], 'domain_name': 'owa.tecfinance.pt', 'geoip_country': 'Denmark'}
"""

@bp.cli.command('export_dnstwist')
def export_dnstwist():
    """ Exporta a lista de dominios gerados pelo DNSTwist """
    #app.logger.info("Iniciand0...") 
    #dnstwist = DNSTwist.query.all()
    #Exportamos apenas os dominios dnstwist e nao os dominios legitimos
    query = db.session.query(DNSTwist)
    sub_query = db.session.query(Domains.domain_name)
    query = query.filter(~DNSTwist.domain_name.in_(sub_query))
    for d in query:
        print(d.domain_name)


app.register_blueprint(bp)