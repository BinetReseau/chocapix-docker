import requests
import json
from flask import Flask, request
app = Flask(__name__)

proxy = {'http': "http://kuzh.polytechnique.fr:8080"}


@app.route("/ooshop/<path:q>")
def get(q):
    r = requests.get("http://mshop.carrefour.com/convertigo/projects/ooshop/%s%s" % (q, ("?" + request.query_string if request.query_string else "")), proxies=proxy)
    return r.text


@app.route("/intermarche/login", methods=['POST'])
def login():
    headers = {'Msq-App':'mcom.ios.smartphone', 'Msq-Jeton-App': '0e74eb93-d2e1-4df6-a386-c84ed874638d'}
    r = requests.post("https://ws-rg-prd.mousquetaires.com/ReferentielMetaService/v1/login", headers = headers, json = request.json, proxies=proxy)
    return r.text

@app.route("/intermarche/orders")
def orders():
    headers = {'Msq-App':'mcom.ios.smartphone', 'Msq-Jeton-App': '0e74eb93-d2e1-4df6-a386-c84ed874638d', 'Content-Type': 'application/json', 'Tokenauthentification': request.args.get('token', '')}
    r = requests.get("http://wsmcommerce.intermarche.com/api/v1/client/commande?enCours=true&historique=true&nombre=10", headers = headers, proxies=proxy)
    return r.text

@app.route("/intermarche/details", methods=['POST'])
def idetails():
    headers = {'Msq-App':'mcom.ios.smartphone', 'Msq-Jeton-App': '0e74eb93-d2e1-4df6-a386-c84ed874638d', 'Content-Type': 'application/json', 'Tokenauthentification': request.args.get('token', '')}
    r = requests.post("https://ws-mz-prd.mousquetaires.com/repo-mcom/rest/produits/ids/97", headers = headers, json = request.json, proxies=proxy)
    return r.text

if __name__ == "__main__":
    app.run()
