
## Installation
python3 -m pip install --upgrade pip
python3 -m venv env (PS> virtualenv env)
source env/bin/activate (PS> .\env\Scripts\activate.bat)
pip3 install -r requirements.txt
* export set FLASK_APP=sites.webapp (PS> $env:FLASK_APP="sites.webapp")
* python3 -m flask run --host=0.0.0.0 (PS> flask run)