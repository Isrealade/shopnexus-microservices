# 🛒 ShopNexus

A modern, microservices-based e-commerce platform designed for scalability, performance, and a seamless shopping experience.

---

## 🏗️ Architecture Overview

```mermaid
graph TD
    Client[Client Browser] --> Frontend[Frontend Service<br/>Next.js]
    Frontend --> UserService[User Service<br/>Flask]
    Frontend --> ProductService[Product Service<br/>Flask]
    UserService --> Redis[(Redis Cache)]
    ProductService --> Redis
    UserService --> PostgreSQL[(PostgreSQL)]
    ProductService --> PostgreSQL
    MetricsSim[Metrics Simulator] --> Prometheus[Prometheus]
    Prometheus --> Grafana[Grafana]
```

---

## 📦 Services

- **Frontend Service ([frontend/](frontend/))**
  - Built with Next.js and TypeScript
  - Server-side rendering
  - Jest testing setup
  - Docker containerization
  - API documentation in `API.md`

- **User Service ([user-service/](user-service/))**
  - Flask-based REST API
  - Handles user management, authentication, and profiles
  - Docker containerization
  - Unit tests in `tests/` directory
  - API documentation in `API.md`

- **Product Service ([product-service/](product-service/))**
  - Flask-based REST API
  - Manages product catalog, inventory, and recommendations
  - Docker containerization
  - Unit tests in `tests/` directory
  - API documentation in `API.md`

- **Metrics Simulator ([metrics-simulator/](metrics-simulator/))**
  - Python-based metrics generator
  - Simulates Prometheus metrics for testing monitoring pipelines
  - Docker containerization
  - Detailed documentation in `README.md`

- **Observability Stack**
  - **Monitoring ([observability/monitoring/](observability/monitoring/))**
    - Prometheus configuration
    - Grafana dashboards
    - Pre-configured monitoring views:
      1. **Node Exporter Dashboard**
         - URL: [Node Exporter for Prometheus](https://grafana.com/grafana/dashboards/15172-node-exporter-for-prometheus-dashboard-based-on-11074/)
         - Monitors system metrics like CPU, memory, disk, and network usage
      2. **cAdvisor Dashboard**
         - URL: [Docker Container Monitoring](https://grafana.com/grafana/dashboards/19908-docker-container-monitoring-with-prometheus-and-cadvisor/)
         - Monitors container metrics like CPU, memory, and network usage
         - Note: When running on Docker Desktop, cAdvisor metrics may be limited due to the containerization layer
  - **Logging ([observability/logging/](observability/logging/))**
    - Centralized logging configuration
    - Log aggregation setup

---

## 🛠️ Infrastructure

- **PostgreSQL**: Persistent storage for users and products
- **Redis**: Caching, session storage, and rate limiting
- **Docker Compose**: 
  - `docker-compose.yml`: Core services
  - `docker-compose.obs.yml`: Observability stack
  - `docker-compose.services.yml`: Additional services
- **GitHub Actions**: CI/CD workflows in `.github/workflows/`

---

## 🚀 Getting Started

### 1. Clone the Repository

```sh
git clone https://github.com/isrealade/shopnexus-microservices.git
cd shopnexus-microservices
```

### 2. Install Dependencies

- **Frontend:**  
  ```sh
  cd frontend && npm install
  ```
- **User Service:**  
  ```sh
  cd ../user-service && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
  ```
- **Product Service:**  
  ```sh
  cd ../product-service && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
  ```

### 3. Environment Variables

The project includes example environment files (`.env.example`) for all services with development defaults. You can use these directly for local development:

```sh
# Copy example files to create your environment files
cp .env.example .env.db
cp frontend/.env.example frontend/.env
cp user-service/.env.example user-service/.env
cp product-service/.env.example product-service/.env
cp observability/monitoring/grafana/.env.example observability/monitoring/grafana/.env
cp observability/logging/elasticsearch/.env.example observability/logging/elasticsearch/.env
cp observability/logging/kibana/.env.example observability/logging/kibana/.env
```

> **Note**: The example environment files contain development defaults. For production deployment, make sure to change all passwords and sensitive values.

Required environment files:
- **Root:** `.env` (Database and Redis configuration)
- **Frontend:** `.env` in `frontend/`
- **User Service:** `.env` in `user-service/`
- **Product Service:** `.env` in `product-service/`
- **Observability Stack:**
  - **Grafana:** `.env` in `observability/monitoring/grafana/`
  - **Elasticsearch:** `.env` in `observability/logging/elasticsearch/`
  - **Kibana:** `.env` in `observability/logging/kibana/`

Example configuration:
```env
# Frontend Service
NEXT_PUBLIC_API_URL=http://localhost:3000
NEXT_PUBLIC_USER_SERVICE_URL=http://localhost:5001
NEXT_PUBLIC_PRODUCT_SERVICE_URL=http://localhost:5002

# User Service
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://shopnexus:shopnexus123@postgres:5432/users
REDIS_URL=redis://redis:6379

# Product Service
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://shopnexus:shopnexus123@postgres:5432/products
REDIS_URL=redis://redis:6379

# Grafana
GF_SECURITY_ADMIN_USER=admin
GF_SECURITY_ADMIN_PASSWORD=admin
GF_USERS_ALLOW_SIGN_UP=false

# Elasticsearch
ELASTIC_PASSWORD=changeme
ELASTIC_USERNAME=elastic

# Kibana
ELASTICSEARCH_HOSTS=http://elasticsearch:9200
ELASTICSEARCH_USERNAME=elastic
ELASTICSEARCH_PASSWORD=changeme
```

### 4. Start Services

You have two options to start the services:

#### Option 1: Start Everything at Once
This will start all services, including the metrics simulator and observability stack:

```sh
docker-compose up --build
```

#### Option 2: Start Services Individually
This approach gives you more control over which services to run:

1. First, start the observability stack:
```sh
docker-compose -f docker-compose.obs.yml up -d
```

2. Then, start the core services:
```sh
docker-compose -f docker-compose.services.yml up -d
```

3. (Optional) If you want to run the metrics simulator:
```sh
cd metrics-simulator
docker build -t metrics-simulator .
docker run -d --network shopnexus_shopnexus-net metrics-simulator
```

### 5. Access the Services

- Frontend: [http://localhost:3000](http://localhost:3000)
- User Service: [http://localhost:5001](http://localhost:5001)
- Product Service: [http://localhost:5002](http://localhost:5002)
- Prometheus: [http://localhost:9090](http://localhost:9090)
- Grafana: [http://localhost:3001](http://localhost:3001)

---

## 🧪 Running Tests

- **Frontend:**  
  ```sh
  cd frontend && npm test
  ```
- **User Service:**  
  ```sh
  cd user-service && python -m unittest discover tests
  ```
- **Product Service:**  
  ```sh
  cd product-service && python -m unittest discover tests
  ```

---

## 📖 API Documentation

- Frontend API documentation: [frontend/API.md](frontend/API.md)
- User Service API documentation: [user-service/API.md](user-service/API.md)
- Product Service API documentation: [product-service/API.md](product-service/API.md)

---

## 📂 Project Structure

```
.
├── docker-compose.yml              # Main Docker Compose configuration
├── docker-compose.obs.yml         # Observability stack configuration (Prometheus, Grafana, etc.)
├── docker-compose.services.yml    # Microservices configuration
├── init-multiple-dbs.sh           # Database initialization script
├── frontend/                      # Frontend application (Next.js)
│   ├── components/                # Reusable UI components
│   ├── pages/                     # Application routes and views
│   ├── __tests__/                 # Unit and integration tests (Jest)
│   └── API.md                     # Frontend API documentation
├── user-service/                  # User management service (Flask)
│   ├── app.py                     # Main Flask application
│   ├── tests/                     # Unit tests
│   ├── requirements.txt           # Python dependencies
│   └── API.md                     # API documentation
├── product-service/               # Product management service (Flask)
│   ├── app.py                     # Main Flask application
│   ├── tests/                     # Unit tests
│   ├── requirements.txt           # Python dependencies
│   └── API.md                     # API documentation
├── metrics-simulator/             # Metrics simulator service
│   ├── app.py                     # Metrics generation logic
│   └── README.md                  # Service documentation
├── observability/                 # Monitoring and logging
│   ├── monitoring/                # Prometheus and Grafana setup
│   └── logging/                   # Logging stack (e.g., Fluent Bit, Loki)
└── .github/                       # GitHub Actions workflows
    ├── actions/                   # Custom GitHub Actions
    └── workflows/                 # CI/CD workflow definitions

```

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

For major changes, please open an issue first to discuss what you would like to change.

---

## 🛣️ Roadmap

- [x] Microservices architecture
- [x] Dockerized development
- [x] Observability stack (monitoring/logging)
- [x] Metrics simulation
- [ ] Distributed tracing
- [ ] Advanced alerting
- [ ] Performance optimization
- [ ] Security enhancements

---

## 📝 License

[MIT](LICENSE)
