from flask import Flask, jsonify, request
import os
from flasgger import Swagger, swag_from
import requests

# Initialiser Flask og Flasgger
app = Flask(__name__)
swagger = Swagger(app)

# Base URLs for microservices
MICROSERVICES = {
    "abonnement": "http://abonnement-service:5001",
    "faktura": "http://faktura-service:5002",
    "fleet": "http://fleet-service:5003",
    "kunde": "http://kunde-service:5004",
    "skade": "http://skade-service:5005",
}

# Helper funktion til at sende requests videre
def proxy_request(service, endpoint):
    try:
        url = f"{MICROSERVICES[service]}/{endpoint}"
        headers = {
            key: value for key, value in request.headers if key.lower() != 'host'
        }
        
        # Ensure Content-Type is set for non-GET requests
        if request.method != 'GET':
            headers['Content-Type'] = 'application/json'

        response = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            json=request.get_json() if request.method != 'GET' else None,
            params=request.args
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Home route
@app.route('/')
@swag_from('swagger/home.yaml')
def home():
    services_info = {}
    for service_name, service_url in MICROSERVICES.items():
        try:
            response = requests.get(f"{service_url}/")
            if response.status_code == 200:
                service_data = response.json()
                available_endpoints = []

                # Fetch endpoints dynamically
                endpoints = service_data.get("endpoints", service_data.get("available_endpoints", []))
                for endpoint in endpoints:
                    path = endpoint.get("path", "").replace("<int:", "").replace(">", "")
                    method = endpoint.get("method", "").lower()
                    description = endpoint.get("description", "No description available")

                    # Generate Swagger path
                    operation_name = path.strip('/').replace('/', '_')
                    swagger_url = f"/apidocs/#/{service_name.capitalize()}/{method}_api_{service_name}_{operation_name}"

                    available_endpoints.append({
                        "path": swagger_url,
                        "method": endpoint.get("method", ""),
                        "description": description
                    })

                services_info[service_name] = {
                    "service": service_data.get("service"),
                    "available_endpoints": available_endpoints
                }
            else:
                services_info[service_name] = {"error": f"Service responded with status code {response.status_code}"}
        except requests.ConnectionError:
            services_info[service_name] = {"error": "Service unavailable"}

    return jsonify({
        "message": "API Gateway is running",
        "services": services_info
    })

# ---- Abonnement Microservice Routes ----
@app.route('/api/abonnement/create_subscription', methods=['POST'])
@swag_from('swagger/abonnement/proxy_create_subscription.yaml')
def abonnement_create():
    return proxy_request("abonnement", "create_subscription")

@app.route('/api/abonnement/get_subscription/abonnement_id', methods=['GET'])
@swag_from('swagger/abonnement/proxy_get_subscription.yaml')
def abonnement_get(abonnement_id):
    return proxy_request("abonnement", f"get_subscription/{abonnement_id}")

@app.route('/api/abonnement/delete_subscription/abonnement_id', methods=['DELETE'])
@swag_from('swagger/abonnement/proxy_delete_subscription.yaml')
def abonnement_delete(abonnement_id):
    return proxy_request("abonnement", f"delete_subscription/{abonnement_id}")

@app.route('/api/abonnement/update_status/<int:abonnement_id>', methods=['PATCH'])
@swag_from('swagger/abonnement/proxy_update_status.yaml')
def abonnement_update(abonnement_id):
    return proxy_request("abonnement", f"update_status/{abonnement_id}")

@app.route('/api/abonnement/report', methods=['GET'])
@swag_from('swagger/abonnement/proxy_report.yaml')
def abonnement_report():
    return proxy_request("abonnement", "report")

# ---- Faktura Microservice Routes ----
@app.route('/api/faktura/create_invoice', methods=['POST'])
@swag_from('swagger/faktura/proxy_create_invoice.yaml')
def faktura_create():
    return proxy_request("faktura", "create_invoice")

@app.route('/api/faktura/get_invoice/faktura_id', methods=['GET'])
@swag_from('swagger/faktura/proxy_get_invoice.yaml')
def faktura_get(faktura_id):
    return proxy_request("faktura", f"get_invoice/{faktura_id}")

@app.route('/api/faktura/update_status/faktura_id', methods=['PUT'])
@swag_from('swagger/faktura/proxy_update_status.yaml')
def faktura_update(faktura_id):
    return proxy_request("faktura", f"update_status/{faktura_id}")

@app.route('/api/faktura/report', methods=['GET'])
@swag_from('swagger/faktura/proxy_report.yaml')
def faktura_report():
    return proxy_request("faktura", "report")

# ---- Fleet Microservice Routes ----
@app.route('/api/fleet/create_vehicle', methods=['POST'])
@swag_from('swagger/fleet/proxy_create_vehicle.yaml')
def fleet_create():
    return proxy_request("fleet", "create_vehicle")

@app.route('/api/fleet/get_vehicle/bil_id', methods=['GET'])
@swag_from('swagger/fleet/proxy_get_vehicle.yaml')
def fleet_get(vehicle_id):
    return proxy_request("fleet", f"get_vehicle/{vehicle_id}")

@app.route('/api/fleet/update_vehicle/bil_id', methods=['PUT'])
@swag_from('swagger/fleet/proxy_update_vehicle.yaml')
def fleet_update(vehicle_id):
    return proxy_request("fleet", f"update_vehicle/{vehicle_id}")

@app.route('/api/fleet/delete_vehicle/bil_id', methods=['DELETE'])
@swag_from('swagger/fleet/proxy_delete_vehicle.yaml')
def fleet_delete(vehicle_id):
    return proxy_request("fleet", f"delete_vehicle/{vehicle_id}")

@app.route('/api/fleet/list_vehicles', methods=['GET'])
@swag_from('swagger/fleet/proxy_list_vehicles.yaml')
def fleet_list():
    return proxy_request("fleet", "list_vehicles")

# ---- Kunde Microservice Routes ----
@app.route('/api/kunde/create_customer', methods=['POST'])
@swag_from('swagger/kunde/proxy_create_customer.yaml')
def kunde_create():
    return proxy_request("kunde", "create_customer")

@app.route('/api/kunde/get_customer/kunde_id', methods=['GET'])
@swag_from('swagger/kunde/proxy_get_customer.yaml')
def kunde_get(kunde_id):
    return proxy_request("kunde", f"get_customer/{kunde_id}")

@app.route('/api/kunde/update_status/kunde_id', methods=['PUT'])
@swag_from('swagger/kunde/proxy_update_status.yaml')
def kunde_update(kunde_id):
    return proxy_request("kunde", f"update_status/{kunde_id}")

@app.route('/api/kunde/report', methods=['GET'])
@swag_from('swagger/kunde/proxy_report.yaml')
def kunde_report():
    return proxy_request("kunde", "report")

# ---- Skade Microservice Routes ----
@app.route('/api/skade/create_skade', methods=['POST'])
@swag_from('swagger/skade/proxy_create_skade.yaml')
def skade_create():
    return proxy_request("skade", "create_skade")

@app.route('/api/skade/get_skade/skade_id', methods=['GET'])
@swag_from('swagger/skade/proxy_get_skade.yaml')
def skade_get(skade_id):
    return proxy_request("skade", f"get_skade/{skade_id}")

@app.route('/api/skade/update_skade/skade_id', methods=['PUT'])
@swag_from('swagger/skade/proxy_update_skade.yaml')
def skade_update(skade_id):
    return proxy_request("skade", f"update_skade/{skade_id}")

@app.route('/api/skade/delete_skade/skade_id', methods=['DELETE'])
@swag_from('swagger/skade/proxy_delete_skade.yaml')
def skade_delete(skade_id):
    return proxy_request("skade", f"delete_skade/{skade_id}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)