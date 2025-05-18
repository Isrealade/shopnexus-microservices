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
```

---

## 📦 Services

- **Frontend Service ([frontend/](frontend/))**
  - Built with Next.js (React)
  - Server-side rendering
  - Connects to backend APIs

- **User Service ([user-service/](user-service/))**
  - Flask-based REST API
  - Handles user management, authentication, and profiles

- **Product Service ([product-service/](product-service/))**
  - Flask-based REST API
  - Manages product catalog, inventory, and recommendations

---

## 🛠️ Infrastructure

- **PostgreSQL**: Persistent storage for users and products
- **Redis**: Caching, session storage, and rate limiting
- **Docker Compose**: Orchestrates all services for local development

---

## 🚀 Getting Started

### 1. Clone the Repository

```sh
git clone https://github.com/isrealade/shopnexus-microservices.git
cd shopnexus
```

### 2. Install Dependencies

- **Frontend:**  
  ```sh
  cd frontend && npm install
  ```
- **User Service:**  
  ```sh
  cd ../user-service && pip install -r requirements.txt
  ```
- **Product Service:**  
  ```sh
  cd ../product-service && pip install -r requirements.txt
  ```

### 3. Environment Variables

Create the following `.env` files:

- **Database:** `.env.db` in the root
- **Frontend:** `.env` in `frontend/`
- **User Service:** `.env.user-service` in `user-service/`
- **Product Service:** `.env.product-service` in `product-service/`

Example:
```env
# Frontend Service
NEXT_PUBLIC_API_URL=http://localhost:3000

# User Service
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://user:password@postgres:5432/users
REDIS_URL=redis://redis:6379

# Product Service
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://user:password@postgres:5432/products
REDIS_URL=redis://redis:6379
```

### 4. Start All Services

```sh
docker-compose up --build
```

- Frontend: [http://localhost:3000](http://localhost:3000)
- User Service: [http://localhost:5001](http://localhost:5001)
- Product Service: [http://localhost:5002](http://localhost:5002)

---

## 🧪 Running Tests

- **Frontend:**  
  ```sh
  cd frontend && npm test
  ```
- **User Service:**  
  ```sh
  cd user-service && python -m unittest tests/test_app.py
  ```
- **Product Service:**  
  ```sh
  cd product-service && python -m unittest tests/test_app.py
  ```

---

## 📖 API Documentation

Each service contains its own API documentation. See:

- [frontend/pages/](frontend/pages/)
- [user-service/](user-service/)
- [product-service/](product-service/)

---

## 📂 Project Structure

```
.
├── docker-compose.yml
├── init-multiple-dbs.sh
├── .env.db
├── frontend/
│   ├── components/
│   ├── pages/
│   └── ...
├── user-service/
│   ├── app.py
│   ├── tests/
│   └── ...
├── product-service/
│   ├── app.py
│   ├── tests/
│   └── ...
└── ...
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📝 License

[MIT](LICENSE)

---

## 💡 Credits

Built with ❤️ by the ShopNexus team.