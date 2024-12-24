# api-gateway-service

The api-gateway-service is a Flask-based microservice that acts as a central entry point for routing requests to various microservices. This API Gateway is deployed on Microsoft Azure and handles request forwarding, load distribution, and response aggregation for microservices such as abonnement, faktura, fleet, kunde, and skade. The service ensures seamless communication between services and secures incoming requests.

## Features
	•	Request Proxying: Forwards incoming API requests to the appropriate microservice.
	•	Endpoint Aggregation: Provides a unified endpoint structure for all connected services.
	•	Azure Deployment: Hosted on Azure Web Apps for high availability and scalability.
	•	Swagger API Documentation: Fully documented endpoints for development and testing.
	•	Microservice Routing: Routes to multiple services, including abonnement, faktura, fleet, kunde, and skade.
	•	Error Handling: Manages unavailable services by returning clear error responses.

## Azure Deployment URLs

The following services are deployed on Azure and are accessible via these URLs:

	•	API Gateway: https://bilabonnement-hqeeh0che9a2bwcs.northeurope-01.azurewebsites.net
	•	Abonnement Service: https://abonnement-service-dcdtaafbcdecdzgb.northeurope-01.azurewebsites.net
	•	Faktura Service: https://faktura-service-afhzcfcgbtdjfbg0.northeurope-01.azurewebsites.net
	•	Kunde Service: https://kunde-service-fhguhvbva6anfvfw.northeurope-01.azurewebsites.net
	•	Skade Service: https://skade-service-h9e9g6d4eab5cheh.northeurope-01.azurewebsites.net

## Requirements

### Python Packages
	•	Python 3.7 or higher
	•	Flask
	•	Flask-Swagger (Flasgger)
	•	python-dotenv
	•	Flask-CORS
    •	requests

### Python Dependencies

Install the required dependencies using:
```pip install -r requirements.txt```

### Environment Variables

Create a .env file in the root directory and specify the following:
```
FLASK_DEBUG=1
```

## Getting Started

1.	Ensure Azure Services are Running

    Verify that all microservices are running on their respective Azure Web App URLs.

2.	Start the API Gateway Locally

    To run the API Gateway locally for testing and development, use the following command:

Run the Flask application:
```python api_gateway.py```
The gateway will be available at http://127.0.0.1:8000.

To deploy updates to Azure, push changes to the main branch, and the Azure Web App deployment will trigger automatically via GitHub Actions.

## Docker

### Build and Run with Docker

To containerize and run the API Gateway, follow these steps:

	1.	Build the Docker Image

    Navigate to the root directory of the project (where the Dockerfile is located) and run:
```docker build -t api-gateway-service .```

	2.	Run the Container
```docker run -d -p 8000:8000 --env-file .env api-gateway-service```

	•	-d: Runs the container in detached mode.
	•	-p 8000:8000: Maps port 8000 of the container to port 8000 on the host machine.
	•	--env-file .env: Loads environment variables from the .env file.

The API Gateway will now be available at http://localhost:8000.

## Docker-Compose (Optional for Multi-Service Deployment)

To orchestrate and run the API Gateway alongside other microservices:
	1.	docker-compose.yaml Example:
```
version: '3.8'
services:
  api-gateway:
    build: .
    ports:
      - "8000:8000"
    env_file: 
      - .env
    depends_on:
      - abonnement-service
      - faktura-service
      - kunde-service
      - fleet-service
      - skade-service

  abonnement-service:
    image: birklauritzen/abonnement-service:latest
    ports:
      - "5001:5001"

  faktura-service:
    image: birklauritzen/faktura-service:latest
    ports:
      - "5002:5002"
```
	2.	Run with Docker Compose
```docker-compose up -d```

### Stop Containers
```docker-compose down```

## Pushing to Docker Hub (Optional)
	1.	Tag the image:
```docker tag api-gateway-service birklauritzen/api-gateway-service:latest```

	2.	Push the image:
```docker push birklauritzen/api-gateway-service:latest```

## API Endpoints

1. GET /

Provides a list of available endpoints across all connected microservices.

#### Response Example:
```
{
  "message": "API Gateway is running",
  "services": {
    "abonnement": {"status": "Available", "endpoints": ["/create_subscription", "/get_subscription/<int:id>"]},
    "faktura": {"status": "Available", "endpoints": ["/create_invoice", "/get_invoice/<int:id>"]},
    "fleet": {"status": "Available", "endpoints": ["/create_vehicle", "/get_vehicle/<int:id>"]},
    "kunde": {"status": "Available", "endpoints": ["/create_customer", "/get_customer/<int:id>"]},
    "skade": {"status": "Available", "endpoints": ["/create_skade", "/get_skade/<int:id>"]}
  }
}
```

2. POST /api/abonnement/create_subscription

Forwards the request to create a new subscription in the abonnement service.

#### Request Body Example:
```
{
  "customer_id": 101,
  "vehicle_id": 202,
  "start_date": "2024-01-01"
}
```

3. GET /api/faktura/get_invoice/int:id

Fetches an invoice by ID from the faktura service.

#### Response Example:
```
{
  "id": 5,
  "customer_id": 456,
  "amount": 1200.50,
  "status": "Paid"
}
```

4. PATCH /api/fleet/update_vehicle/int:id

Updates vehicle details in the fleet service.

#### Request Body:
```
{
  "status": "Available",
  "mileage": 20000
}
```

## Project Structure
```
.
├── api_gateway.py        # Main Flask application
├── swagger/              # YAML files for API documentation
│   ├── abonnement/
│   ├── faktura/
│   ├── fleet/
│   ├── kunde/
│   ├── skade/
│   └── home.yaml
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker container setup
├── docker-compose.yaml   # Docker-Compose configuration for deployment
├── .env                  # Environment variables
└── README.md             # Project documentation
```
## Azure Deployment
	•	The API Gateway and all microservices are deployed using Azure Web Apps for scalability and reliability.
	•	Continuous Deployment is set up through GitHub Actions, which automatically deploys changes when pushed to the repository.

## Development Notes

### Swagger Documentation
	•	Swagger Documentation: Accessible at /apidocs after running the application.
	•	Error Handling: The gateway returns 500 errors if any microservice is unreachable.
	•	CORS Support: Configured to allow requests from all origins. Update as necessary for production environments.

## Contributions

Feel free to fork the repository and submit pull requests. For major changes, open an issue to discuss modifications.

## License

This project is licensed under the MIT License. See LICENSE for more information.