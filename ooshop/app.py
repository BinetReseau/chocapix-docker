import requests
from flask import Flask, request
app = Flask(__name__)

proxy = {'http': "http://kuzh.polytechnique.fr:8080"}

@app.route("/<path:q>")
def get(q):
    r = requests.get("http://mshop.carrefour.com/convertigo/projects/ooshop/%s%s" % (q, ("?" + request.query_string if request.query_string else "")), proxies=proxy)
    return r.text

if __name__ == "__main__":
    app.run()
