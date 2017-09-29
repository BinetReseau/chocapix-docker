import requests
import json
from flask import Flask, request, abort
app = Flask(__name__)

# proxy = {'http': "http://kuzh.polytechnique.fr:8080"}


# ===== OOSHOP (Carrefour) =====

@app.route("/ooshop/<path:q>")
def ooshop(q):
    r = requests.get("http://mshop.carrefour.com/convertigo/projects/ooshop/%s%s" % (q, ("?" + request.query_string if request.query_string else "")), proxies=proxy)
    return r.text



# ===== INTERMARCHE =====

@app.route("/intermarche/login", methods=['POST'])
def intermarcheLogin():
    headers = {'Msq-App':'mcom.ios.smartphone', 'Msq-Jeton-App': '0e74eb93-d2e1-4df6-a386-c84ed874638d'}
    r = requests.post("https://ws-rg-prd.mousquetaires.com/ReferentielMetaService/v1/login", headers = headers, json = request.json) #, proxies=proxy)
    return r.text

@app.route("/intermarche/orders")
def intermarcheOrders():
    headers = {'Msq-App':'mcom.ios.smartphone', 'Msq-Jeton-App': '0e74eb93-d2e1-4df6-a386-c84ed874638d', 'Content-Type': 'application/json', 'Tokenauthentification': request.args.get('token', '')}
    r = requests.get("http://wsmcommerce.intermarche.com/api/v1/client/commande?enCours=true&historique=true&nombre=10", headers = headers) #, proxies=proxy)
    return r.text

@app.route("/intermarche/details", methods=['POST'])
def intermarcheDetails():
    headers = {'Msq-App':'mcom.ios.smartphone', 'Msq-Jeton-App': '0e74eb93-d2e1-4df6-a386-c84ed874638d', 'Content-Type': 'application/json', 'Tokenauthentification': request.args.get('token', '')}
    r = requests.post("https://ws-mz-prd.mousquetaires.com/repo-mcom/rest/produits/ids/97", headers = headers, json = request.json) #, proxies=proxy)
    return r.text



# ===== PICARD =====

@app.route("/picard/login", methods=['POST'])
def picardLogin():
    headers = {'Ods-Mobile-Id':'F4286248-A27C-4C4C-A18A-344F1C442F2A', 'User-Agent': 'Picard/1.1.1.13 (iPhone; iOS 9.2.1; Scale/2.00)'}
    data = [{"target" : "/picard/loginU", "serial" : "1", "map": request.json}]
    r = requests.post("https://ods.ocito.com/ods/picard/iphone/", headers = headers, json = data) #, proxies=proxy)
    return json.dumps(r.json()[0]['map'])
    # return r.text

@app.route("/picard/orders")
def picardOrders():
    headers = {'Ods-Mobile-Id':'F4286248-A27C-4C4C-A18A-344F1C442F2A', 'User-Agent': 'Picard/1.1.1.13 (iPhone; iOS 9.2.1; Scale/2.00)'}
    data = [{"target" : "/picard/orders/show", "serial" : "1", "map": {"session": request.headers.get('Authorization', '')}}]
    r = requests.post("https://ods.ocito.com/ods/picard/iphone/", headers = headers, json = data) #, proxies=proxy)
    return json.dumps(r.json()[0]['data'])

@app.route("/picard/orders/<id>")
def picardOrder(id):
    headers = {'Ods-Mobile-Id':'F4286248-A27C-4C4C-A18A-344F1C442F2A', 'User-Agent': 'Picard/1.1.1.13 (iPhone; iOS 9.2.1; Scale/2.00)'}
    # We must get all orders again, because I did not find a route to get one specific order
    data = [{"target" : "/picard/orders/show", "serial" : "1", "map": {"session": request.headers.get('Authorization', '')}}]
    r = requests.post("https://ods.ocito.com/ods/picard/iphone/", headers = headers, json = data) #, proxies=proxy)

    orders = r.json()[0]['data']['data']
    order = None
    for o in orders:
        if 'order_no' in o and o['order_no'] == id:
            order = o
            break
    if order is None:
        abort(404)

    for p in order['product_items']:
        data = [{"target" : "/picard/produit", "serial" : "1", "map": {"warehouseCode" : "", "idProduit" : p['product_id']}}]
        r = requests.post("https://ods.ocito.com/ods/picard/iphone/", headers = headers, json = data) #, proxies=proxy)
        p['details'] = r.json()[0]['data']

    return json.dumps(order)

@app.route("/picard/product/<id>")
def picardProduct(id):
    headers = {'Ods-Mobile-Id':'F4286248-A27C-4C4C-A18A-344F1C442F2A', 'User-Agent': 'Picard/1.1.1.13 (iPhone; iOS 9.2.1; Scale/2.00)'}
    data = [{"target" : "/picard/produit", "serial" : "1", "map": {"warehouseCode" : "", "idProduit" : id}}]
    r = requests.post("https://ods.ocito.com/ods/picard/iphone/", headers = headers, json = data) #, proxies=proxy)
    return json.dumps(r.json()[0]['data'])



# ===== HOURA (Cora) =====

@app.route("/houra/<path:url>", methods=['POST'])
def houraLogin(url):
    headers = {'Content-Type':'application/json;charset=utf-8', 'X-Houra-Application-Id': 'Tiv1.1.2', 'X-Houra-Device-Uuid': 'uuid'}
    rget = requests.post("http://www.houra.fr/ws_mobile/%s" % url, headers = headers, json = request.json) #, proxies=proxy)
    return rget.text

if __name__ == "__main__":
    app.run()
