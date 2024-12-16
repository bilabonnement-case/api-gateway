from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Base URLs for microservices
MICROSERVICES = {
    "abonnement": "http://abonnement-service:5001",
    "faktura": "http://fakturering-service:5002",
    "fleet": "http://fleet-service:5003",
    "kunde": "http://kunde-service:5004",
    "skade": "http://skade-service:5005",
}

# Route til abonnement-microservice
@app.route('/api/abonnement/<path:endpoint>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def abonnement_proxy(endpoint):
    return proxy_request("abonnement", endpoint)

# Route til faktura-microservice
@app.route('/api/faktura/<path:endpoint>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def faktura_proxy(endpoint):
    return proxy_request("faktura", endpoint)

# Route til fleet-microservice
@app.route('/api/fleet/<path:endpoint>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def fleet_proxy(endpoint):
    return proxy_request("fleet", endpoint)

# Route til kunde-microservice
@app.route('/api/kunde/<path:endpoint>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def kunde_proxy(endpoint):
    return proxy_request("kunde", endpoint)

# Route til skade-microservice
@app.route('/api/skade/<path:endpoint>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def skade_proxy(endpoint):
    return proxy_request("skade", endpoint)

# Helper-funktion til at videresende requests
def proxy_request(service, endpoint):
    try:
        url = f"{MICROSERVICES[service]}/{endpoint}"
        response = requests.request(
            method=request.method,
            url=url,
            headers={key: value for key, value in request.headers if key != 'Host'},
            json=request.get_json(),
            params=request.args,
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Home route
@app.route('/')
def home():
    return jsonify({"message": "API Gateway is running", "services": list(MICROSERVICES.keys())})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)