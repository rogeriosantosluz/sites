# Sites

Trata-se de um template para gerenciar sites desenvolvido em Flask. 

## Dependencias

* Flask==1.1.2
* Flask-Bootstrap4==4.0.2
* SQLAlchemy==1.3.19
* Flask-SQLAlchemy==2.4.4
* Flask-Migrate==2.5.3
* python-dotenv==0.14.0

## Instalação

* python3 -m pip install --upgrade pip
* python3 -m venv env (PS> virtualenv env)
* source env/bin/activate (PS> .\env\Scripts\activate.bat)
* pip3 install -r requirements.txt
* export set FLASK_APP=sites.webapp (PS> $env:FLASK_APP="sites.webapp")
* export FLASK_ENV=development (default é production)
* python3 -m flask run --host=0.0.0.0 (PS> flask run)

* Criar o arquivo .env na raiz com as seguintes informações:

    * SECRET_KEY = b'sua chave secreta'
    * ADMIN_USERNAME = 'Seu usuario administrador'
    * ADMIN_PASSWORD = 'Uma senha'