import requests
from flask import Flask
app = Flask(__name__)

proxy = {'http': "http://kuzh.polytechnique.fr:8080"}

@app.route("/<barcode>")
def get(barcode):
    r = requests.get("http://fr.openfoodfacts.org/api/v0/produit/%s.json" % barcode, proxies=proxy)
    return r.text

if __name__ == "__main__":
    app.run()
